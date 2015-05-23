from flask.ext.wtf import Form
from wtforms import Field, StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo

from harpy_network.models.characters import Character

class NotEqualTo(object):
    """
    Compares the values of two fields.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data == other.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext('Field must not be equal to %(other_name)s.')

            raise ValidationError(message % d)

class CharacterField(Field):

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = Character.query.filter_by(id=valuelist[0]).first()


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class ChangePasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password',
                                                                             message="The Passwords do not match.")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])


class AddCharacterForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(max=254)])

class AddBoonForm(Form):
    debtor = CharacterField("Debtor", validators=[DataRequired(),
                                                  NotEqualTo('creditor',
                                                             message="The Debtor cannot be the same as the Creditor.")])
    creditor = CharacterField("Creditor", validators=[DataRequired()])
    boon_weight = SelectField("Boon Weight",
                              choices=[("trivial", "Trivial Boon"),
                                          ("minor", "Minor Boon"),
                                          ("major", "Major Boon"),
                                          ("blood", "Blood Boon"),
                                          ("life", "Life Boon"),
                                      ],
                              validators=[DataRequired()])
    comment = TextAreaField("Comments", validators=[])

from flask.ext.wtf import Form
from wtforms import Field, StringField, PasswordField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo

from harpy_network.models.characters import Character
from harpy_network.models.status import status_traits


def unique_character_name(form, field):
    character = Character.query.filter_by(name=field.data).first()
    if character:
        if hasattr(form, 'id') and character.id == int(form.id.data):
            pass
        else:
            raise ValidationError('Kindred name is already in use.')


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
    name = StringField('Name', validators=[DataRequired(), Length(max=254), unique_character_name])


class EditCharacterForm(Form):
    id = HiddenField('ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(max=254), unique_character_name])


class MergeCharacterForm(Form):
    merging_kindred = CharacterField("Creditor", validators=[DataRequired()])


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


class EditBoonForm(Form):
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


status_choices = [(status_trait.name,
                   "{STATUS_NAME} ({STATUS_TYPE})".format(STATUS_NAME=status_trait.name, STATUS_TYPE=status_trait.type))
                  for status_trait in status_traits]


class AddStatusForm(Form):
    name = SelectField("Status Trait", choices=status_choices, validators=[DataRequired()])
    location_earned = StringField('Location Earned', validators=[Length(max=254)])
    story = TextAreaField("Story/Details", validators=[])


class EditStatusForm(Form):
    name = SelectField("Status Trait", choices=status_choices, validators=[DataRequired()])
    location_earned = StringField('Location Earned', validators=[Length(max=254)])
    story = TextAreaField("Story/Details", validators=[])
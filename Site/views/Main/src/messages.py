class Error:
    name = 'error'
    length = 'The {name} must contain between {min} and {max} characters'
    required = 'This field is required.'
    password = 'Passowrd don\'t match'
    generic = 'Sorry but something went wrong, try again.'
    passw_error = 'Username and Password don\'t match!'
    username_error = 'Username has already registered.'
    confirm_mail = 'First confirm your email.'
    existing_mail = 'Exists another user with the same email.'
    link_expired = 'The confirmation link is invalid or has expired.'

class Success:
    name = 'success'
    sent_mail = 'A confirmation email has been sent via email.'
    first_cofirm = 'You have confirmed your account. Thanks!'
    confirmed = 'Account already confirmed. Please login.'
    password_reset = 'Password successfully reset'
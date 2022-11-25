from itsdangerous import URLSafeTimedSerializer

from Site import Config

class LinkAccount:
    @staticmethod
    def confirm_token(token):
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

        data = serializer.loads(
            token,
            salt=Config.SECRET_KEY,
            max_age=600
        )

        return data.split(';')

    @staticmethod
    def generate_confirmation_token(email):
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

        return serializer.dumps("{};{}".format(email), 
            salt=Config.SECRET_KEY)

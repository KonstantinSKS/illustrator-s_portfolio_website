# import os
# from dotenv import load_dotenv

from victoria_site import app  # , db
# from victoria_site.models import User

# load_dotenv()

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()

    #     existing_user = User.query.filter_by(email=os.getenv('EMAIL')).first()
    #     if not existing_user:
    #         new_user = User(
    #             role=os.getenv('ROLE'),
    #             username=os.getenv('USERNAME'),
    #             email=os.getenv('EMAIL'),
    #             password=os.getenv('PASSWORD')
    #         )
    #         db.session.add(new_user)
    #         db.session.commit()
    app.run(port=5000, host="0.0.0.0")

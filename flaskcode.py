# Import Flask
from flask import render_template, Flask

# Video: https://www.youtube.com/watch?v=kng-mJJby8g
# Syntax sources: https://www.digitalocean.com/community/tutorials/how-to-create-your-first-web-application-using-flask-and-python-3
# https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

# Let user enter username and password

# Setting up the website
website = Flask(__name__)

# Using the html file to add things onto the website


@website.route('/')
def use_html():
    return render_template('index.html')


# Running the code to make the website
if __name__ == '__main__':
    website.run(debug=True)

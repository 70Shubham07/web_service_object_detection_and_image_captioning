from flask import Flask

# from flask_wtf.csrf import CSRFProtect


app = Flask (__name__, instance_relative_config=True)

# csrf = CSRFProtect(app)


print( "This is app config: \n", app.config )
if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

    print( "app config after loading from_object: \n", app.config )

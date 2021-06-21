from sqlalchemy.sql.functions import user
from ridwan import create_app
from ridwan.models import User
from sqlalchemy import event

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
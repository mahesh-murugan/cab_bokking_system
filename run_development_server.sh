
# creating virtual environment
python3 -m venv booking_system_evenv

# activating virtual env
source booking_system_evenv/bin/activate

#change directory to project folder 
cd cab_booking_project

# installing all the requirements file in virtual environment
pip install -r requirements.txt

# run development server 
python manage.py runserver

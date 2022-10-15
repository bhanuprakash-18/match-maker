from flask import Flask, render_template, request
import pandas as pd
import matchmaker
app = Flask(__name__)


@app.route("/")
def home():
    cgd = pd.read_excel("cgd.xlsx")

    return render_template("home.html")


@app.route("/match", methods=["GET", "POST"])
def match():
    client_id = request.form['client_id']
    clientname = request.form['clientname']
    age = request.form['age']
    phonenumber = request.form['phonenumber']
    gender = request.form['gender']
    pincode = request.form['pincode']
    language = request.form['language']
    weight = request.form['weight']
    height = request.form['height']
    shifts = request.form['shifts']
    personal_care = request.form['personal_care']
    nanny_care = request.form['nanny_care']
    critical_care = request.form['critical_care']
    nursing_care = request.form['nursing_care']
    services_cd = [personal_care, nanny_care, critical_care, nursing_care]
    no_days_services_required = request.form['no_days_services_required']
    client_data = {'client_id': client_id, 'clientname': clientname, 'age': age, 'phonenumber': phonenumber, 'gender': gender, 'pincode': pincode,
                   'language': language, 'weight': weight, 'height': height, 'shifts': shifts, 'services_cd': services_cd, 'no_days_services_required': no_days_services_required}
    the_output, note = matchmaker.matchcaregiver(
        client_data)[0], matchmaker.matchcaregiver(client_data)[1]
    matched_caregiver_ids = [x for x in the_output.id]
    matched_caregiver_names = [x for x in the_output.name]
    matched_caregiver_ages = [x for x in the_output.age]
    matched_caregiver_genders = [x for x in the_output.gender]
    matched_caregiver_addresses = [x for x in the_output.address]
    matched_caregiver_experiences = [x for x in the_output.experience]
    matched_caregiver_ratings = [x for x in the_output.rating]
    matched_list = list(zip(matched_caregiver_ids, matched_caregiver_names, matched_caregiver_ages,
                        matched_caregiver_genders, matched_caregiver_addresses, matched_caregiver_experiences, matched_caregiver_ratings))
    number_of_matchings_found = len(matched_list)

    return render_template("result.html", result=[matched_list, number_of_matchings_found, note])


if __name__ == '__main__':
    app.run(debug=True)

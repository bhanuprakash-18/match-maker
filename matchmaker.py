import pandas as pd


def matchcaregiver(client_data):
    client_id = client_data['client_id']
    clientname = client_data['clientname']
    age = int(client_data['age'])
    phonenumber = client_data['phonenumber']
    gender = client_data['gender']
    pincode = int(client_data['pincode'])
    language = client_data['language']
    weight = client_data['weight']
    height = client_data['height']
    shifts = int(client_data['shifts'])
    services_cd = client_data['services_cd']
    no_days_services_required = int(client_data['no_days_services_required'])

    care_giver_data = pd.read_excel("cgd.xlsx")
    care_giver_data.columns = ['id', 'name', 'age', 'gender', 'address', 'pincode', 'language',
                               'weight', 'height', 'status', 'experience', 'availability', 'shifts',
                               'rating', 'certification', 'personalcare', 'nannycare',
                               'criticalcare', 'nursingcare']

    cgd = care_giver_data
    note_selection_criteria = ''
    note_not_selection_criteria = ''
    cgd['personalcare'] = [x.lower() for x in cgd['personalcare']]
    cgd['nannycare'] = [x.lower() for x in cgd['nannycare']]
    cgd['criticalcare'] = [x.lower() for x in cgd['criticalcare']]
    cgd['nursingcare'] = [x.lower() for x in cgd['nursingcare']]
    cgd['status'] = [x.lower() for x in cgd['status']]
    # matching based on services required and availability status
    a, b, c, d = [x == 'no' for x in services_cd]
    services = ['personalcare', 'nannycare', 'criticalcare', 'nursingcare']
    matched_status = cgd.loc[cgd['status'] == 'free']

    perfect_matched_services = matched_status.loc[(((a) | (matched_status[services[0]] == 'yes')) & ((b) | (
        matched_status[services[1]] == 'yes')) & ((c) | (matched_status[services[2]] == 'yes')) & ((d) | (matched_status[services[3]] == 'yes')))]
    the_output = perfect_matched_services
    note_selection_criteria += 'services, availability status,'

    # matching based on number of days services required
    if perfect_matched_services.shape[0] > 0:
        matched_availability_days = perfect_matched_services.loc[
            no_days_services_required <= perfect_matched_services['availability']]
        if matched_availability_days.shape[0] > 0:
            the_output = matched_availability_days
            note_selection_criteria += ', number of days services required'
        else:
            note_not_selection_criteria += ', number of days services required'
    # matching based on closer districts and states
    if the_output.shape[0] > 0:
        matched_pincode = the_output.loc[(
            abs(pincode-the_output['pincode']) < 100000)]
        if matched_pincode.shape[0] > 0:
            the_output = matched_pincode
            note_selection_criteria += ', location of closer districts or states'
        else:
            note_not_selection_criteria += ', location of closer districts or states'
    # matching based on language
    if the_output.shape[0] > 0:
        the_output['language'] = [x.lower() for x in the_output['language']]
        matched_language = the_output.loc[language.lower(
        ) == the_output['language']]
        if matched_language.shape[0] > 0:
            the_output = matched_language
            note_selection_criteria += ', language'
        else:
            note_not_selection_criteria += ', language'

    # matching based on shifts
    if the_output.shape[0] > 0:
        matched_shifts = the_output.loc[shifts == the_output['shifts']]
        if matched_shifts.shape[0] > 0:
            the_output = matched_shifts
            note_selection_criteria += ', shifts'
        else:
            note_not_selection_criteria += ', shifts'

    # matching based on near locations
    if the_output.shape[0] > 0:
        matched_closest_pincode = the_output.loc[(
            abs(pincode-the_output['pincode']) < 5000)]
        if matched_closest_pincode.shape[0] > 0:
            the_output = matched_closest_pincode
            note_selection_criteria += ', nearer locations'
        else:
            note_not_selection_criteria += ', nearer locations'

    # matching based on gender
    if the_output.shape[0] > 0:
        matched_gender = the_output.loc[gender == the_output['gender']]
        if matched_gender.shape[0] > 0:
            the_output = matched_gender
            note_selection_criteria += ', gender'
        else:
            note_not_selection_criteria += ', gender'

    # matching based on rating and experience
    if the_output.shape[0] > 0:
        matched_rating_exp = the_output.loc[(max(the_output['rating']) == the_output['rating']) | (
            max(the_output['experience']) == the_output['experience'])]
        if matched_rating_exp.shape[0] > 0:
            the_output = matched_rating_exp
            note_selection_criteria += ', rating, experience'
        else:
            note_not_selection_criteria += ', rating, experience'

    note_selection_criteria = 'The selection of care givers is based on ' + \
        note_selection_criteria + '.'
    if len(note_not_selection_criteria) == 0:
        note_not_selection_criteria = 'Congratulations!!! You have found the Best Matching'
    else:
        note_not_selection_criteria = 'The matchings found are not based on ' + \
            note_not_selection_criteria[1:] + '.'
    # The final care giver data that matched to the given client
    output = [the_output, note_not_selection_criteria]
    if the_output.shape[0] > 0:
        return output
    else:
        return "NO MATCHING FOUND"

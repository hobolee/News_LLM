import openai
import csv
import pandas as pd


def pass2gpt(template):
    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": template}
        ]
    )

    print(response)
    print(response.choices[0]['message']['content'])
    return response


def wirter2csv(response, data, i):
    # write the result to csv file
    response = response.choices[0]['message']['content']
    response = response.split("Environmental risk:")
    response = response[1].split("Location:")
    data.loc[i, 'is_risk'] = response[0]
    response = response[1].split("Time:")
    data.loc[i, 'location'] = response[0]
    response = response[1].split("What is the risk:")
    data.loc[i, 'time'] = response[0]
    response = response[1].split("Result:")
    data.loc[i, 'what_is_risk'] = response[0]
    response = response[1].split("Why the result:")
    data.loc[i, 'result'] = response[0]
    response = response[1].split("Specific advice:")
    data.loc[i, 'why'] = response[0]
    data.loc[i, 'specific_advice'] = response[1]
    return data


# config the openai api
openai.api_type = "azure"
openai.api_base = "https://hkust.azure-api.net/"
openai.api_version = "2023-05-15"
openai.api_key = "2593cee0e1b94c4f8ba138d996efb038"
openai.temprature = 0.2

# load the csv file
data = pd.read_csv("data_output.csv", encoding='utf_8_sig')
# data.insert(len(data.columns), 'is_risk', 0)
# data.insert(len(data.columns), 'location', 0)
# data.insert(len(data.columns), 'time', 0)
# data.insert(len(data.columns), 'what_is_risk', 0)
# data.insert(len(data.columns), 'result', 0)
# data.insert(len(data.columns), 'why', 0)
# data.insert(len(data.columns), 'specific_advice', 0)
# print(data.head())
# print(data.shape)
# print(data['内容'][0])
content = data['内容'][0]

template = "Here is a strict template to output in English based on the news. [ouput]Environmental risk: Yes or no. Location: the detailed place. Time: specific time including hours if indicated. What is the risk: several words. Result: several words. Why the result: several words. Specific advice: several sentences. (Attention: the output are case sensitive) "

try:
    for i in range(46, 50):
        print(i)
        content = data['内容'][i]
        prompt = template + "News: " + content
        response = pass2gpt(prompt)
        data = wirter2csv(response, data, i)
except Exception as e:
    print(e)
    data.to_csv("data_output.csv", encoding='utf_8_sig', index=False)  # to do: just add the row

data.to_csv("data_output.csv", encoding='utf_8_sig', index=False) # to do: just add the row
pass

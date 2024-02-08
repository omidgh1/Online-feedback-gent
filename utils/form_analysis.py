def percentage_radio(df,var,chosen):
    try:
        return round((int(df[var].value_counts()[chosen])/int(df[var].value_counts().sum()))*100,2)
    except:
        return round((int(1)/int(df[var].value_counts().sum()))*100,2)

def analysis_radio(df,var,section,chosen):
    h_often_percent = percentage_radio(df, var, chosen)
    text = f"{chosen} has been chosen by {str(h_often_percent)}% of people about the {section} like you."
    return text


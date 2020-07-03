def wordsPerMinuteFeedback(wordsPerMinute):
    string = "Your WPM score (= words per minute) is {:.3f}.\n".format(wordsPerMinute)
    string += (
        "With the WPM (= words per minute) we can determine, if you talk too fast or too slow.\n"
        "An average person speaks about 100 - 130 words per minute.\n")

    if wordsPerMinute > 130:
        string += (
            "As you can see, your WPM is above the average speaking rate of a person.\n"
            "Speeking too fast will make it harder for your audience to understand you.\n"
            "Also this can be an indication, that you are too nervous in your presentation.\n"
            "Remember to take regular speech breaks, so that the audience can process what they heard!")
    elif wordsPerMinute < 110:
        string += (
            "As you can see, your WPM is below the average speaking rate of a person.\n"
            "It's mostly better to talk too slow, rather than to fast.\n"
            "However, talking too slow may cause your listeners to get bored quickly and not to pay\n"
            "attention to your presentation.")
    else:
        string += "Your speaking speed is balanced!"

    return string
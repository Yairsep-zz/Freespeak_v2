def voiceEmotionsFeedback(color_number, color_names, output_path):
    indexMaxVal = findAllIndices(color_number)
    occuringEmotions = "We detected these emotions in your voice:\n"
    emotions = ""
    for i in range(len(color_names)):
        if(color_number[i] != 0):
            emotions += "-" + color_names[i] + "\n"
    occuringEmotions += emotions + "\n"
    fearfulIndex = 0
    for i in range(0, len(color_names)):
        if color_names[i] == "fearful":
            fearfulIndex = i
            break
    if "fearful" in color_names:
        if fearfulIndex in indexMaxVal:
            occuringEmotions += (
                "\nFear was one of the most common emotions during your speaking.\n"
                "Here are some tips for better presenting voice:\n"
                "1.If you're new to public speaking, try to start small, find a few friends or family members to practice on and just build up.\n"
                "2.The size of the audience is not that important. The most important thing is your knowledge of the topic about which\n"
                "you are presenting. If you know it really well you'll get more confidence and this is really important! The ability to connect\n"
                "with your audience comes from having the confidence and you won't get lost during a presentation.\n"
                "3.Don't just to memorize word for word of your entire speech, you have to understand it from the beginning until the end.\n"
                "4.The most fearful moment is awaiting your presentation. Just think about a perfect ending and throw bad thoughts away!:)")
        else:
            occuringEmotions +=  (
                "\nWe detected some fear, but it was not one of the emotions that occurred the most.\n"
                "Maybe you have some sections, where you still don't feel confident in.\n"
                "Try practicing your 'weak spots' extensively because confidence is key!\n"
                "You could write down some hints on a small card to fall back on, but try not to memorize your speech word by word!\n"
                "Understanding your topic thoroughly can give you that extra confidence boost that you need!\n")

    if "happy" in color_names:
        occuringEmotions += (
            "\nGood job! Your voice sounded happy!\n"
            "A happy voice can trick yourself to be more motivated for your presentation.\n"
            "Happiness will make you seem more likeable for your audience and you will have more fun presenting!\n")

    if "calm" in color_names:
        occuringEmotions += (
            "\nYour voice was calm. That's great!\n"
            "A calm voice makes it easy for your audience to understand you.\n"
            "Also, you will seem confident with a calm voice.\n"
            "However, remember to mix up the emotions, so your audience doesn't get bored!\n")
    else:
        occuringEmotions += (
            "\We didn't record your voice being calm. You can sound calmer if you speak slowly.\n"
            "Cour voice will have more power and authority and your listeners will have an opportunity\n"
            "to absorb and reflect on what you're saying. Powerful people speak slowly, enunciate clearly, and express themselves with confidence.\n")

    occuringEmotions += tipsForImprovement()

    saveToText(occuringEmotions, output_path)

def tipsForImprovement():
    occuringEmotions = (
        "\nRemember to speak slowly during your presentation. When you speak rapidly, your pitch increases and you sound more fearful."
        "A loud, confident and slow speaking voice will lead you to a powerful and moving speech!\n"
        "Also, the power of your speech is contained in the silences that you create as you speak. Put more pauses in your speaking to create more effect.\n"
        "And last but not least don't forget to drink and to eat before presenting! Energy is essential for good speaking and voice projection!\n")
    return occuringEmotions

def saveToText(comment, output_path):
    text_file = open(output_path + "\\speechEmotionsTippsAndAdvices.txt", "w")
    text_file.write(comment)
    text_file.close()

def findAllIndices(color_number):
    maxVal = -1
    positionsMaxVal = []
    for i in range(len(color_number)):
        if maxVal <= color_number[i]:
            maxVal = color_number[i]
            positionsMaxVal.append(i)
    return positionsMaxVal

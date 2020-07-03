def faceEmotionsFeedback(output_path):
    string = (
        "The movements of your eyes, mouth, and facial muscles can build a connection with your audience.\n"
        "Alternatively, they can undermine your every word. Eye focus is the most important element in this process.\n"
        "Effective presenters engage one person at a time, focusing long enough to complete a natural phrase and watch it sink in for a moment.\n"
        "The other elements of facial expression can convey the feelings of the presenter, anything from passion for the subject, to depth of concern for the audience.\n"
        "Unfortunately, under the pressure of delivering a group presentation, many people lose their facial expression.\n"
        "Their faces solidify into a grim, stone statue, a thin straight line where the lips meet.\n"
        "Try to unfreeze your face right from the start. For example, when you greet the audience, smile!\n"
        "You won't want to smile throughout the entire presentation, but at least at the appropriate moments.\n"
        "It's only on rare occasions that you may need to be somber and serious throughout.\n"
        "Use your facial expressions as a tool to underline your content!"
    )
    text_file = open(output_path + "\\facialExpressionsAdvices.txt", "w")
    text_file.write(string)
    text_file.close()
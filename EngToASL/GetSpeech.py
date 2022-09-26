import azure.cognitiveservices.speech as speechsdk

def getSpeech():
  # Creates an instance of a speech config with specified subscription key and service region.
  # Replace with your own subscription key and service region (e.g., "westus").
  with open('keys/speech_key.txt','r') as f_open:
      speech_key = f_open.read()
      f_open.close()
  with open('keys/speech_region.txt','r') as f_open:
      service_region = f_open.read()
      f_open.close()

  # Creates an instance of a speech config with specified subscription key and service region.
  # Replace with your own subscription key and service region (e.g., "westus").
  speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

  # Creates a recognizer with the given settings
  speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

  print("Say something to translate...")
  result = speech_recognizer.recognize_once()

  # Checks result.
  if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}\n".format(result.text))
  elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized: {}".format(result.no_match_details))
    quit()
  elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
      print("Error details: {}".format(cancellation_details.error_details))
    quit()

  return result.text
import google.generativeai as genai
import json
import time
import argparse
import os

genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

# Function to translate text using Gemini
def translate(text, target_language):
    model = genai.GenerativeModel("gemini-1.5-flash")  
    try:
        response = model.generate_content(
            f"""You are a translator API. Your task is to translate the following text.

CRITICAL INSTRUCTIONS:
1. Translate the entire text as is, without adding or removing any characters or placeholders.
2. Do NOT add any curly braces {{ }} that are not in the original text.
3. Provide ONLY the translated text as your response.
4. Do NOT include any markdown formatting, quotation marks, backticks, or extra newline characters in your response.
5. Preserve the exact structure and formatting of the original text.

Original text (in English):
{text}

Translate the above text to {target_language}. Remember, provide ONLY the direct translation without any modifications to the structure or added characters."""
        )
        print(response)
        if response.parts:
            return response.parts[0].text.strip()
        else:
            raise ValueError("No translation generated")
    except Exception as e:
        print(f"Translation error for '{text}': {str(e)}")
        return text  # Return original text if translation fails

def main():
    parser = argparse.ArgumentParser(description="Translate JSON file using Gemini API")
    parser.add_argument("input_file", choices=["geneva.json", "moonchain.json"], help="Input JSON file to translate")
    args = parser.parse_args()

    language_dict = {
        "de": "German",
        "es": "Español",
        "fr": "Français",
        "it": "Italiano",
        "ko": "Korean",
        "nl": "Dutch",
        "ro": "Romanian",
        "tr": "Turkish",
        "zh-hans": "Chinese Simplified",
        "zh-hant": "Chinese Traditional",
        "id": "Indonesian",
        "pt": "Portuguese",
        "vi": "Vietnamese",
        "ja": "Japanese",
        "ru": "Russian"
    }

    # Read the input JSON file
    with open(args.input_file, 'r') as file:
        data = json.load(file)

    # Get the English content
    en_content = data["en"][0]

    # Loop through each language in the dictionary
    for lang_code, lang_name in language_dict.items():
        # Translate title, excerpt, and content
        translated_title = translate(en_content["title"], lang_name)
        translated_excerpt = translate(en_content["excerpt"], lang_name)
        translated_content = translate(en_content["content"], lang_name)

        # Create the translated entry
        translated_entry = {
            "title": translated_title,
            "excerpt": translated_excerpt,
            "content": translated_content
        }

        # Add the translated entry to the data
        data[lang_code] = [translated_entry]

        time.sleep(10)  # Pause for a bit between each language translation

    # Write the updated data back to the file
    with open(args.input_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print(f"Translation complete. Check the '{args.input_file}' file.")

if __name__ == '__main__':
    main()

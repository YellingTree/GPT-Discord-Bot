import os
import json
import config
import openai
openai.api_key = config.openai_api_key
class MemoryManagment():
    async def get_conversation(server_id: str):
        conversation = await _IO.manage_file(server_id, "r")
        return(conversation)
    async def save_conversation(server_id: str, conversation):
        await _IO.manage_file(server_id, "w", conversation)
    def crop_conversation(conversation: list):
        conversation = conversation[-config.old_msg_removal_amount:]
        return(conversation)

class ResponseManagemnt():
    async def _api_request(messages:list):
        response = openai.ChatCompletion.create(
            model = config.chat_model,
            messages = messages,
            max_tokens = config.token_limit,
            n = config.creation_amount,
            logit_bias = config.bias,
            top_p = config.top_prob
        )
        return(response['choices'][0]['message']['content'])
    async def create_response(server_id: str, conversation, user_message):
        processing_error = False
        messages = conversation + [user_message]
        try:
            response = await ResponseManagemnt._api_request(messages)
        except openai.error.InvalidRequestError as e:
            if 'tokens' in str(e):
                conversation = MemoryManagment.crop_conversation(conversation)
                messages = conversation + [user_message]
                response = await ResponseManagemnt._api_request(messages)
            else:
                response = "An unknown error has occurred."
                processing_error = True
        except openai.error.RateLimitError as e:
            response = "The response generation is being rate-limited, try again later."
            processing_error = config.remove_error_messages
        except openai.error.OpenAIError as e:
            response = "An error has occurred on OpenAI server. try again later."    
            processing_error = config.remove_error_messages
        return(response, processing_error)
    async def create_messages(server_id: str, response: str, conversation: list, user_message, failstate):
        if response == "" or response == " ":
            response = "Generated an empty message."
            failstate = config.delete_empty_messages
        if failstate:
            await MemoryManagment.save_conversation(server_id, conversation)
        else:
            updated_conversation = conversation + [user_message, {"role": "assistant", "content": response}]
            await MemoryManagment.save_conversation(server_id, updated_conversation)
        message_blocks = []
        if len(response) < config.max_characters:
            message_blocks.append(response)
        else:
            i=0
            while i < len(response):
                block = response[i:i+config.max_characters]
                message_blocks.append(block)
                i += config.max_characters
        return(message_blocks)

class _IO():
    async def _file_check(server_id: str):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        chats_dir = os.path.join(current_dir, "chats")
        if not os.path.exists(chats_dir):
            os.makedirs(chats_dir)
        file_path = os.path.join(chats_dir, str(server_id) + ".json")
        if not os.path.exists(file_path):
            with open(file_path, "w") as conversation_file:
                json.dump([], conversation_file)
        return(file_path)
    
    async def manage_file(server_id: str, operation: str, data: list = []):
        file_path = await _IO._file_check(server_id)
        if operation == "w" or operation == "a":
            with open(file_path, operation) as managed_file:
                json.dump(data, managed_file)
        elif operation == "r":
            with open(file_path, "r") as managed_file:
                retrieved_data = json.load(managed_file)
                return(retrieved_data)

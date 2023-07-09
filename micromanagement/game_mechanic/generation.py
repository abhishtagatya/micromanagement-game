from micromanagement.util.prompt import MOVEMENT_INSTRUCTION
from micromanagement.interface import OpenAIComplete


class TextGenerationMechanic:

    def __init__(self, token):
        self.openai_client = OpenAIComplete(token=token)

    def generate(self, prompt, instruction=MOVEMENT_INSTRUCTION):
        gen_instruct = ""
        new_instruction = instruction.format(prompt=prompt)
        gen_instruct += self.openai_client.call(new_instruction)
        return gen_instruct

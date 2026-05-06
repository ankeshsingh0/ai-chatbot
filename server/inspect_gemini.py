import google.generativeai as genai
import inspect
print('version', genai.__version__)
print('sig', inspect.signature(genai.GenerativeModel))
# print source first 2000 chars
src=inspect.getsource(genai.GenerativeModel)
print(src[:2000])

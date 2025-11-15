import httpx
import wikipedia
def get_summary(query:str) -> str:
    print("inside the wikepedia")
    """Fetches a short summary from Wikipedia based on the search term."""
    raw_snippet=wikipedia.summary(query)
    print(raw_snippet)
    return raw_snippet


def addition(arg)-> int:
    print("inside addition -->",arg)
    return arg
    
# if __name__=='__main__':
#     # print("DONEEE")
#     get_summary("who is elon musk")
#     # print(resp)
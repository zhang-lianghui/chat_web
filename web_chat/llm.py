from langchain_wenxin.llms import Wenxin

llm = Wenxin(model="ernie-bot-turbo")

def get_ans(question):
    ans = llm.invoke("hello")
    #ans = ans.content
    print(ans)
    
if __name__ == '__main__':
    get_ans('test')
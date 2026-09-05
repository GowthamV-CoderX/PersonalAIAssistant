from app.tools.agent import ask_leny

def main():
    print("Leny is online.")
    
    while(True):
        user_input = input("You:")
        
        if user_input.lower() in {"exit","quit"}:
            print("Leny: Shutting down.")
            break
        
        response = ask_leny(user_input)
        print(f"Leny : {response}")
        

if __name__ == "__main__":
    main()
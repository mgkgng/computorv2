from computor import Computor

if __name__ == "__main__":
    computor = Computor()
    while True:
        try:
            computor.read_input()
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            break
        except EOFError:
            print("\nEOFError")
            break
        except Exception as e:
            print("Error:", e)
            break
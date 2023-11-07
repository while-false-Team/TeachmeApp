import customtkinter as tk

class State:
    def __init__(self, master:tk.CTk, state_manager) -> None:
        self.frame = tk.CTkFrame(master)
        self.end_state = False
        self.push_new_state = False
        self.state_manager_ptr = state_manager

    def pushNewState(self, state):
        self.state_manager_ptr.push_state(state)

    def pushNewDelCur(self, state):
        self.state_manager_ptr.pop_first_state()
        self.state_manager_ptr.push_state(state)

    def delCurrentState(self):
        self.state_manager_ptr.pop_first_state()
    
    def packFrame(self):
        self.frame.pack(fill=tk.BOTH, expand=True)


class State_Manager:
    def __init__(self) -> None:
        self.states = []
    
    def push_state(self, state:State) -> None:
        if len(self.states) > 0:
            self.states[-1].frame.pack_forget()
            self.states.append(state)
            self.states[-1].frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.states.append(state)
            self.states[-1].frame.pack(fill=tk.BOTH, expand=True)
    
    def get_first_state(self) -> State:
        if len(self.states) > 0:
            return self.states[-1]
        else:
            raise BaseException
    
    def pop_first_state(self) -> None:
        if len(self.states) > 1:
            self.states[-1].frame.pack_forget()
            self.states.pop(len(self.states)-1)
            self.states[-1].frame.pack(fill=tk.BOTH, expand=True)
        elif len(self.states) == 1:
            self.states[-1].frame.pack_forget()
            self.states.pop(len(self.states)-1)
        else: 
            pass

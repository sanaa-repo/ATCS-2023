class OpponentFSM:
    def __init__(self):
        self.state = "Idle"
        self.health = 100  # Starting health

    def perform_action(self, action):
        if self.state == "Idle":
            if action == "Attack":
                self.state = "Attack"
                self.perform_attack()
        elif self.state == "Attack":
            if action == "Die":
                self.state = "Dead"
                self.perform_death()
            elif action == "AttackComplete":
                self.state = "Idle"
        elif self.state == "Dead":
            # Handle actions when the opponent is already dead
            pass

    def perform_attack(self):
        print("Performing attack: Kick")
        # Perform kick logic
        # Transition to AttackComplete when the attack is complete
        self.perform_action("AttackComplete")

    def perform_death(self):
        print("Opponent is dead")

# Example usage:
opponent = OpponentFSM()

# Triggering attack
opponent.perform_action("Attack")

# Triggering death (when health reaches zero)
opponent.health = 0
opponent.perform_action("Die")

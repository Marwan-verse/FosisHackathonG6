def run(self):
    running = True
    while running:
        self.handle_events()  # Handle events first

        if self.game_state == "main":
            self.player.update()  # Update player
            self.check_collisions()  # Check collisions
            self.all_sprites.update()  # Update all sprites
            self.all_sprites.draw(self.screen)  # Draw all sprites
        elif self.game_state == "quiz":
            self.run_quiz()  # Run the quiz logic

        pygame.display.flip()
        self.clock.tick(60) 
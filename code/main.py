import pygame,sys,time 
from PIL import Image
from settings import *
from sprites import Player, Ball, Block, Upgrade, Downgrade, Projectile
from surfacemaker import SurfaceMaker
from random import choice, randint
from button import *

class Game:
	def __init__(self):
		 
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

		# background
		self.bg = self.create_bg('../graphics/other/bg2.png')

		# background base
		self.bg_menu = self.create_bg('../graphics/other/bgMenu.png')

		# fonte da tela do menu
		self.font = pygame.font.Font("../fonts/ARCADE_I.TTF", 25)

		# sprite group setup
		self.all_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()
		self.upgrade_sprites = pygame.sprite.Group()
		self.downgrade_sprites = pygame.sprite.Group()
		self.projectile_sprites = pygame.sprite.Group()

		# setup
		self.surfacemaker = SurfaceMaker()
		self.player = Player(self.all_sprites,self.surfacemaker)
		self.stage_setup()
		self.ball = Ball(self.all_sprites,self.player,self.block_sprites)

		# hearts
		self.heart_surf = pygame.image.load('../graphics/other/heart.png').convert_alpha()

		# projectile
		self.projectile_surf = pygame.image.load('../graphics/other/projectile.png').convert_alpha()
		self.can_shoot = False
		self.shoot_time = 0

		self.laser_sound = pygame.mixer.Sound('../sounds/laser.wav')
		self.laser_sound.set_volume(0.1)

		self.powerup_sound = pygame.mixer.Sound('../sounds/powerup.wav')
		self.powerup_sound.set_volume(0.1)

		self.laserhit_sound = pygame.mixer.Sound('../sounds/laser_hit.wav')
		self.laserhit_sound.set_volume(0.02)

		self.game_over = pygame.mixer.Sound('../sounds/game_over.wav')
		self.game_over.set_volume(0.05)

		self.music = pygame.mixer.Sound('../sounds/music.wav')
		self.music.set_volume(0.05)
		self.music.play(loops = -1)

	def create_upgrade(self,pos):
		upgrade_type = choice(UPGRADES)
		Upgrade(pos,upgrade_type,[self.all_sprites,self.upgrade_sprites])
	
	def create_downgrade(self,pos):
		downgrade_type = choice(DOWNGRADES)
		Downgrade(pos, downgrade_type,[self.all_sprites,self.downgrade_sprites])
		

	def create_bg(self, image):
		bg_original = pygame.image.load(image).convert()
		scale_factor_height = WINDOW_HEIGHT / bg_original.get_height()
		scale_factor_width = WINDOW_WIDTH / bg_original.get_width()
		scaled_width = bg_original.get_width() * scale_factor_width
		scaled_height = bg_original.get_height() * scale_factor_height
		scaled_bg = pygame.transform.scale(bg_original,(scaled_width,scaled_height)) 
		return scaled_bg

	def stage_setup(self):
		# cycle through all rows and columns of BLOCK MAP
		for row_index, row in enumerate(BLOCK_MAP):
			for col_index, col in enumerate(row):
				if col != ' ':
					# find the x and y position for each individual block
					x = col_index * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE // 2
					y = TOP_OFFSET + row_index * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2
					Block(col,(x,y),[self.all_sprites,self.block_sprites],self.surfacemaker,self.create_upgrade,self.create_downgrade)

	def display_hearts(self):
		for i in range(self.player.hearts):
			x = 2 + i * (self.heart_surf.get_width() + 2)
			self.display_surface.blit(self.heart_surf,(x,4))

	def upgrade_collision(self):
		overlap_sprites = pygame.sprite.spritecollide(self.player,self.upgrade_sprites,True)
		for sprite in overlap_sprites:
			self.player.upgrade(sprite.upgrade_type)
			self.powerup_sound.play()
	
	def downgrade_collision(self):
		overlap_sprintes = pygame.sprite.spritecollide(self.player,self.downgrade_sprites,True)
		for sprite in overlap_sprintes:
			self.player.downgrade(sprite.downgrade_type)
			self.powerup_sound.play()

	def create_projectile(self):
		if self.player.laser_rects:
			self.laser_sound.play()
		for projectile in self.player.laser_rects:
			Projectile(
				projectile.midtop - pygame.math.Vector2(0,30),
				self.projectile_surf,
				[self.all_sprites, self.projectile_sprites])

	def laser_timer(self):
		if pygame.time.get_ticks() - self.shoot_time >= 500:
			self.can_shoot = True

	def projectile_block_collision(self):
		for projectile in self.projectile_sprites:
			overlap_sprites  = pygame.sprite.spritecollide(projectile,self.block_sprites,False)
			if overlap_sprites:
				for sprite in overlap_sprites:
					sprite.get_damage(1)
				projectile.kill()
				self.laserhit_sound.play()

	def run(self):
		last_time = time.time()
		pygame.display.set_caption("Arknoid")
		run = True
		while run:

			# delta time
			dt = time.time() - last_time
			last_time = time.time()

			# event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.ball.active = True
						if self.can_shoot:
							self.create_projectile()
							self.can_shoot = False
							self.shoot_time = pygame.time.get_ticks()
			if self.player.hearts <= 0:
				self.game_over_screen()

			# draw bg
			self.display_surface.blit(self.bg,(0,0))

			# update the game
			self.all_sprites.update(dt)
			self.upgrade_collision()
			self.downgrade_collision()
			self.laser_timer()
			self.projectile_block_collision()

			# draw the frame
			self.all_sprites.draw(self.display_surface)
			self.display_hearts()

			# update window
			pygame.display.flip()
	
	def quit(self):
		self.music.stop()
		pygame.quit()
		sys.exit()

	def main_menu(self):
		pygame.display.set_caption("Menu")
		
	# setup
		start_button = Button(800, 200, 200, 50, "Start", action=game.run)
		quit_button = Button(800, 300, 200, 50, "Quit", action=game.quit)
		buttons = [start_button, quit_button]

    # Loop principal
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:  # Botão esquerdo do mouse
						for button in buttons:
							if button.is_clicked(event.pos):
								button.action()
				for button in buttons:
					button.handle_event(event)

        # Desenhar a tela
			self.display_surface.blit(self.bg_menu,(0,0))
			for button in buttons:
				button.draw(self.display_surface)

		# Desenhar texto na tela
			text_surface = self.font.render("GALAXY ARKA", True, (255, 255, 255))
			text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 120))
			self.display_surface.blit(text_surface, text_rect)

        # Atualizar a tela
			pygame.display.flip()

	def restart(self):
		self.__init__()
		self.run()

	def game_over_screen(self):
		pygame.display.set_caption("Game Over")

	# setup
		restart_button = Button(800, 200, 200, 50, "Restart", action=game.restart)
		quit_button = Button(800, 300, 200, 50, "Quit", action=game.quit)
		buttons = [restart_button, quit_button]

    # Loop principal
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:  # Botão esquerdo do mouse
						for button in buttons:
							if button.is_clicked(event.pos):
								button.action()
				for button in buttons:
					button.handle_event(event)

        # Desenhar a tela
			self.display_surface.blit(self.bg_menu,(0,0))
			for button in buttons:
				button.draw(self.display_surface)

		# Desenhar texto na tela
			text_surface = self.font.render("GAME OVER", True, (255, 255, 255))
			text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 120))
			self.display_surface.blit(text_surface, text_rect)

        # Atualizar a tela
			pygame.display.flip()

if __name__ == '__main__':
	game = Game()
	game.main_menu()

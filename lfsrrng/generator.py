
class Generator:
	def __init__(self, seed, size=16, taps=[0, 2, 3, 5]) -> None:
		self.__size = size
		self.__taps = taps

		self.set_seed(seed)

		self.__as_bin = lambda x : f"{x:0{self.__size}b}"


	@staticmethod
	def __translate(value, leftMin, leftMax, rightMin, rightMax):
		# Figure out how 'wide' each range is
		leftSpan = leftMax - leftMin
		rightSpan = rightMax - rightMin

		# Convert the left range into a 0-1 range (float)
		valueScaled = float(value - leftMin) / float(leftSpan)

		# Convert the 0-1 range into a value in the right range.
		return rightMin + (valueScaled * rightSpan)


	def __clamp_seed(self):
		if self.__seed > self.__max_seed : self.__seed = self.__max_seed
		if self.__seed < 1               : self.__seed = 1

	def __apply_taps(self):
		# feed_back = (self.__register & 1) ^ ((self.__register >> 2) & 1) ^ ((self.__register >> 3) & 1) ^ ((self.__register >> 5) & 1) # xor bits 0, 2, 3, 5
		feed_back = (self.__register >> self.__taps[0]) & 1

		for shift_index in range(1, len(self.__taps)):
			feed_back = feed_back ^ ((self.__register >> self.__taps[shift_index]) & 1)

		return feed_back

	def __next(self):
		bit = self.__register & 1
		feed_back = self.__apply_taps()
		feed_back = feed_back << (self.__size-1)
		self.__register = self.__register >> 1
		self.__register = self.__register | feed_back

		# print(self.as_bin(self.__register), '|', bit)
		return bit


	def set_seed(self, new_seed):
		"""Sets a new seed and reinitialises the generator

		Args:
			new_seed (int): a seed to be used by the generator
		"""
		self.__seed = new_seed
		self.__max_seed = int('1' * self.__size, 2)
		self.__max_period = (2**self.__size)-1
		self.__clamp_seed()

		self.__register = self.__seed
		self.__next()

	def get_seed_range(self):
		"""Return the minimum and maximum value that a seed can have

		Returns:
			tuple[int]: minimum and maximum value that a seed can have
		"""
		return (1, self.__max_seed)


	def range(self, min_val, max_val):
		"""Generates a random number in range min_val and max_val

		Args:
			min_val (int): minimum value to generate from (inclusive)
			max_val (int): maximum value to generate from (exlusive)

		Returns:
			float: a random number between min_val and max_val
		"""
		generator_range = (0, self.__max_seed)
		desired_range = (min_val, max_val)

		value = 0
		for _ in range(self.__size):
			value = value << 1
			value = value | self.__next()

		return self.__translate(value, generator_range[0], generator_range[1], desired_range[0], desired_range[1])

	def choice(self, itterable):
		list_len = len(itterable)
		index = int(self.range(0, list_len))
		return itterable[index]


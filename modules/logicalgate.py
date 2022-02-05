def nand(a,b):
	"""
	Basic NAND logical gate.
	@param a: First entry.
	@param b: Second entry.
	@return: 0 or 1 according to NAND logic.
	"""
	if a and b:
		return 0
	else:
		return 1
		
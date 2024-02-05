extends Path2D

var _followers = []
var _bugtexture = load("res://Assets/bug.png")
var _speed :float = 120.0
@onready var _path2D = get_node("/root/gameField/track")

func _ready():
	pass

func _physics_process(delta):
	
	var finishing = []
	for follower in _followers:
		follower.set_progress(follower.get_progress() + _speed * delta)
		# deal with beatbugs who are back home
		if follower.progress_ratio >= 1.0:			
			follower.queue_free()
			finishing.append(follower)
		
	for follower in finishing:
		_followers.erase(follower)


func _on_spawn_timer_timeout():
	# create a new follower
	var follower
	follower = PathFollow2D.new()
	follower.loop = false
	follower.rotates = false
	var bugsprite = Sprite2D.new()
	bugsprite.texture = load("res://Assets/bug.png")
	follower.add_child(bugsprite)
	
	# assign to path and add to array
	_path2D.add_child(follower)	
	_followers.append(follower)	

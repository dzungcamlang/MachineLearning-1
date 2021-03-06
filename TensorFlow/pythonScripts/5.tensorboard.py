import tensorflow as tf

input_data = [[1,5,3,7,8,10,12],
			[5,8,10,3,9,7,1]]
label = [[0,0,0,1,0],
		[1,0,0,0,0]]


INPUT_SIZE = 7 
HIDDEN1_SIZE = 10
HIDDEN2_SIZE = 8
CLASSES = 5
Learning_Rate = 0.05

x = tf.placeholder(tf.float32, shape=[None,INPUT_SIZE], name='x')
y_ = tf.placeholder(tf.float32, shape=[None,CLASSES], name='y')

feed_dict = {x:input_data, y_:label}

w1 = tf.Variable( tf.truncated_normal(shape=[INPUT_SIZE, HIDDEN1_SIZE], dtype = tf.float32 ), name='w1' )
b1 = tf.Variable( tf.zeros([HIDDEN1_SIZE], dtype = tf.float32), name='b1' )

w2 = tf.Variable( tf.truncated_normal(shape=[HIDDEN1_SIZE, HIDDEN2_SIZE], dtype = tf.float32 ) ,name='w2')
b2 = tf.Variable( tf.zeros([HIDDEN2_SIZE], dtype = tf.float32), dtype = tf.float32, name='b2' )

wo = tf.Variable( tf.truncated_normal(shape=[HIDDEN2_SIZE,CLASSES], dtype = tf.float32 ), name='wo' )
bo = tf.Variable( tf.zeros([CLASSES], dtype = tf.float32 ), name='bo')

param_list = [w1, b1, w2, b2, wo, bo]
saver = tf.train.Saver(param_list)

with tf.name_scope('hidden1') as h1_scope:
	hidden1 = tf.sigmoid(tf.matmul(x, w1) + b1, name='hidden1')
with tf.name_scope('hidden2') as h2_scope:
	hidden2 = tf.sigmoid(tf.matmul(hidden1, w2) + b2, name='hidden2')
with tf.name_scope('output') as o_scope:
	y = tf.sigmoid( tf.matmul( hidden2, wo ) + bo , name='y')

with tf.name_scope('cost') as scope:
	cost = tf.reduce_mean(-y_ * tf.log(y) - (1-y)*tf.log(1-y))

with tf.name_scope('train'):
	train = tf.train.GradientDescentOptimizer(Learning_Rate).minimize(cost)
with tf.name_scope('evaluation'):
	comp_pred = tf.equal(tf.arg_max(y,1) , tf.arg_max(y_, 1 ))
	accuracy = tf.reduce_mean(tf.cast(comp_pred, dtype= tf.float32))

with tf.Session() as sess:
	init = tf.global_variables_initializer() 
	sess.run(init)
	merge = tf.summary.merge_all()
	for step in range(1000):
		_, loss, acc = sess.run([train, cost, accuracy], feed_dict = feed_dict)
		if step % 100 == 0:
			train_writer = tf.summary.FileWriter('../summaries/4.summaries',sess.graph)
			saver.save(sess, "../ckpt/4.model")
			print("step : ",step)
			print("loss : ",loss)
			print("acc : ",acc)


from flask_restful import reqparse
import datetime

problem_post_args = reqparse.RequestParser()
problem_post_args.add_argument("name",type=str,required=True,help='name is required!')
problem_post_args.add_argument("questioner_id",type=int,required=True,help='questioner_id is required!')
problem_post_args.add_argument("source_id",type=int,required=True,help='source_id is required!')
problem_post_args.add_argument("difficulty",type=str,required=True,help='difficulty is required!')
problem_post_args.add_argument("content",type=str,required=True,help='content is required!')
problem_post_args.add_argument("time_limit",type=int,required=True,help='time_limit is required!')
problem_post_args.add_argument("memory_limit",type=int,required=True,help='memory_limit is required!')
problem_post_args.add_argument("is_hidden",type=int,required=True,help='is_hidden is required!')

problem_get_args = reqparse.RequestParser()
problem_get_args.add_argument("page",type=int)
problem_get_args.add_argument("difficulty",type=str)
problem_get_args.add_argument("name",type=str)


problem_put_args = reqparse.RequestParser()
problem_put_args.add_argument("name",type=str)
problem_put_args.add_argument("difficulty",type=int)
problem_put_args.add_argument("content",type=str)
problem_put_args.add_argument("sample_input",type=str)
problem_put_args.add_argument("time_limit",type=int)
problem_put_args.add_argument("memory_limit",type=int)
problem_put_args.add_argument("is_hidden",type=int)
problem_put_args.add_argument("testcase_count",type=int)
problem_put_args.add_argument("correct_source_code",type=str)

test_run_post_args = reqparse.RequestParser()
test_run_post_args.add_argument("user_id", type=int, required=True, help="User_id is required!")
test_run_post_args.add_argument("problem_id", type=int, default=0)
test_run_post_args.add_argument("exam_id", type=int,default=0)
test_run_post_args.add_argument("homework_id", type=int,default=0)
test_run_post_args.add_argument("language", type=str, required=True, help="Language is required!")
test_run_post_args.add_argument("code_content", type=str, required=True, help="Code_content is required!")
test_run_post_args.add_argument("test_case", type=str, required=True, help="Testcase is required!")

create_problem_test_run_args = reqparse.RequestParser()
create_problem_test_run_args.add_argument("user_id", type=int, required=True, help="User_id is required!")
create_problem_test_run_args.add_argument("language", type=str, required=True, help="Language is required!")
create_problem_test_run_args.add_argument("code_content", type=str, required=True, help="Code_content is required!")
create_problem_test_run_args.add_argument("test_case", type=str, required=True, action="append")


signup_post_args = reqparse.RequestParser()
signup_post_args.add_argument("name", type=str, required=True, help='Username is required!')
signup_post_args.add_argument("email", type=str, required=True, help='Email is required!')
signup_post_args.add_argument("password", type=str, required=True, help='Password is required!')
signup_post_args.add_argument("confirm_password", type=str, required=True, help='Confirm_password is required!')

login_post_args = reqparse.RequestParser()
login_post_args.add_argument("email", type=str, required=True, help='Email is required!')
login_post_args.add_argument("password", type=str, required=True, help='Password is required!')
login_post_args.add_argument("remember", type=bool)

user_profile_put_args = reqparse.RequestParser()
user_profile_put_args.add_argument("name", type=str)
user_profile_put_args.add_argument("email", type=str)
user_profile_put_args.add_argument("password", type=str)

request_reset_post_args = reqparse.RequestParser()
request_reset_post_args.add_argument("email", type=str, required=True, help='Email is required!')

confirm_token_post_args = reqparse.RequestParser()
confirm_token_post_args.add_argument("token", type=str, required=True, help="Token is required!")

reset_password_put_args = reqparse.RequestParser()
reset_password_put_args.add_argument("token", type=str, required=True, help='Token is required!')
reset_password_put_args.add_argument("password", type=str, required=True, help='Password is required!')
reset_password_put_args.add_argument("confirm_password", type=str, required=True, help='Confirm_password is required!')


submission_post_args = reqparse.RequestParser()
submission_post_args.add_argument("user_id", type=int, required=True, help="User_id is required!")
submission_post_args.add_argument("problem_id", type=int, required=True, help="Problem_id is required!")
submission_post_args.add_argument("source_id", type=int, required=True, help="Source_id is required!")
submission_post_args.add_argument("status", type=int, required=True, help="Status is required!")
submission_post_args.add_argument("error_hint", type=int)
submission_post_args.add_argument("error_line", type=int)
submission_post_args.add_argument("language", type=str, required=True, help="Language is required!")
submission_post_args.add_argument("time_used", type=str, required=True, help="Time_used is required!")
submission_post_args.add_argument("memory_used", type=str, required=True, help="Memory_used is required!")
submission_post_args.add_argument("exam_id", type=int)
submission_post_args.add_argument("homework_id", type=int)
submission_post_args.add_argument("code_content", type=str, required=True, help="Code_content is required!")

queue_post_args = reqparse.RequestParser()
queue_post_args.add_argument("user_id", type=int, required=True, help="User_id is required!")
queue_post_args.add_argument("problem_id", type=int, default=0)
queue_post_args.add_argument("exam_id", type=int)
queue_post_args.add_argument("homework_id", type=int)
queue_post_args.add_argument("language", type=str, required=True, help="Language is required!")
queue_post_args.add_argument("code_content", type=str, required=True, help="Code_content is required!")

dispatcher_post_args = reqparse.RequestParser()
dispatcher_post_args.add_argument("Return_count", type=int, required=True, help="Return_count is required!")
dispatcher_post_args.add_argument("Return_Set",   type=dict, required=True, help="Return_Set is required!", action="append")

exam_post_args = reqparse.RequestParser()
exam_post_args.add_argument('class_id',type=int,required=True,help="class_id is required!")
exam_post_args.add_argument('user_id',type=int,required=True,help="user_id is required!")
exam_post_args.add_argument('exam_name',type=str,required=True,help="exam_name is required!")
exam_post_args.add_argument('exam_info',type=str,required=True,help="exam_info is required!")
exam_post_args.add_argument('exam_start_time',type=str,required=True,help="exam_start_time is required!")
exam_post_args.add_argument('exam_end_time',type=str,required=True,help="exam_endtime is required!")
exam_post_args.add_argument('problem_set',type=int,required=True,help="problem_set is required!", action="append")

class_post_args = reqparse.RequestParser()
class_post_args.add_argument('user_id',type=int,required=True,help="user_id is required!")
class_post_args.add_argument('class_name',type=str,required=True,help="class_name is required!")
class_post_args.add_argument('semester',type=str,required=True,help="semester is required!")
class_post_args.add_argument('is_public',type=int,required=True,help="is_public is required!")

class_put_args = reqparse.RequestParser()
class_post_args.add_argument('user_id',type=int,required=True,help="user_id is required!")
class_put_args.add_argument('name',type=str)
class_put_args.add_argument('semester',type=str)
class_put_args.add_argument('teacher_name',type=str)
class_put_args.add_argument('is_public',type=int)
class_put_args.add_argument('invite_code',type=str)

class_member_post_args = reqparse.RequestParser()
class_member_post_args.add_argument('user_id',type=int,required=True,help="user_id is required!")
class_member_post_args.add_argument('student_id',type=int,required=True,help="student_id is required!")
class_member_post_args.add_argument('invite_code',type=str,required=True,help="invite_code is required!")

homework_post_args = reqparse.RequestParser()
homework_post_args.add_argument('class_id',type=int,required=True,help="class_id is required!")
homework_post_args.add_argument('user_id',type=int,required=True,help="user_id is required!")
homework_post_args.add_argument('homework_name',type=str,required=True,help="homework_name is required!")
homework_post_args.add_argument('homework_info',type=str,required=True,help="homework_info is required!")
homework_post_args.add_argument('upload_time',type=str,required=True,help="upload_time is required!")
homework_post_args.add_argument('deadline',type=str,required=True,help="deadline is required!")
homework_post_args.add_argument('problem_set',type=int,required=True,help="problem_set is required!", action="append")


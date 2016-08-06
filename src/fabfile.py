from fabric.api import local

def push():
	local('git status')
	print "you can create a separate branch for this changes!"
	
	local('git add -A')
	commit_message = raw_input("Enter commit message:")
	local('git commit -m "%s"'%commit_message)
	branch_name = local('git name-rev --name-only HEAD', capture=True)
	print "Current branch name: %s"%branch_name,
	local('git status')
	local('git push origin %s'%branch_name)


def heroku():
	branch_name = local('git name-rev --name-only HEAD', capture=True)
	print "You are merging %s with master"%branch_name
	local('git checkout master')
	local('git pull origin master --commit')
	local('git merge %s'%branch_name)
	local('git push origin master')
	local('heroku run python src/manage.py migrate')
	local('git checkout %s'%branch_name)
	print "Merging done"
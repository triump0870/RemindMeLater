from fabric.api import local

def push():
	local('git status')
	print "you can create a separate branch for this changes!"
	inp = raw_input("Enter Y to continue:")
	print "inp:",inp
	if inp == "Y" or inp == 'y':
		local('git add .')
		commit_message = raw_input("Enter commit message:")
		local('git commit -m "%s"'%commit_message)
		branch_name = local('git name-rev --name-only HEAD', capture=True)
		print "Current branch name: %s"%branch_name,
		local('git push origin %s'%branch_name)


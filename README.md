# Vkontake comics poster.
### Takes random comics from [xkcd](https://xkcd.com/) and post it to [Vkontakte](https://vk.com)(Russian Facebook.)

## Requirements
Python >= 3.5 required.  
Install dependencies with 
```bash
pip install -r requirements.txt
```
For better interaction is recommended to use [virtualenv](https://github.com/pypa/virtualenv).

## Usage

To run this script you need to:
1. Create account on [Vkontakte](https://vk.com)
2. Create group [VK group administration](https://vk.com/groups?tab=admin)
3. Create application [VK for developers](https://vk.com/dev)
4. Obtain auth token with [VK implicit flow user](https://vk.com/dev/implicit_flow_user)

Then create inside repo directory .env file and fill it with
* vk_group_id (ID of your group, which you've created at step 2.)
* vk_auth_token (Token what you've obtained at step 4.)

Run 
```bash
python main.py
```

## Output
```bash
Comics 175 has been successfully posted.
```

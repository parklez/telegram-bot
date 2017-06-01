#Anime library plugin. /animes, /edit.

from config import *

make_dir('files/animes/')
animes_list_file = 'files/animes.txt'
animes_list = load_dict(animes_list_file)

anime_choice = dict()
new_anime_id = dict()
new_anime_name = dict()

### Anime listing ###
@bot.message_handler(commands=['animes'])
def reply_anime_list(message):
    cid = get_user_id(message)
    
    if cid in users_steps and users_steps[cid] == 'edit_mode':
        markup = types.ForceReply(selective=True)
        msg = bot.reply_to(message, 'Choose the serie to edit.', reply_markup=markup)

        bot.register_next_step_handler(msg, editor_get_anime_id)
    else:
        users_steps[cid] = 'reply_anime_info_and_episodes'
    
    page_input = message.text[7:]
    
    if page_input.isdigit():
        page = int(page_input)
    else:
        page = 0

    ipp = 20 # items per page
    start = ipp * page
    end = start + ipp

    anime_list = sorted(list(animes_list))
    list_len = len(anime_list)
    
    # Check if there are enough elements to fill.
    if list_len - start < ipp:
        keys = int(list_len - start)
    else:
        keys = int(ipp)
        
    counter = 0

    reply_msg = '<b>Available Series:</b>\n'
    for key in range(keys):
        reply_msg += '/' + str(start+counter) + '. ' + anime_list[(start+key)] + '\n'
        counter += 1
    reply_msg += '<b>Choose a number.</b>'
    if int(list_len/ipp) > page:
        reply_msg += '\nNext page: /animes' + str(page+1)
    reply_msg += '\nor hit /close to exit.'
    bot.send_message(message.chat.id, reply_msg, parse_mode='HTML')

help_commands['animes'] = 'Lists all anime series available.'

@bot.message_handler(func=lambda message: get_user_step(get_user_id(message)) == 'reply_anime_info_and_episodes')
def reply_anime_info_and_episodes(message):
    cid = get_user_id(message)
    
    users_steps[cid] = 'reply_anime_episode_download'
    
    anime_id = message.text[1:]
    
    if 'animes' in anime_id:
        users_steps[cid] = ''
        reply_anime_list(message)
        return

    if '@AndreasBOT' in anime_id:
        anime_id = anime_id.strip('@AndreasBOT')

    anime_list = sorted(list(animes_list))
        
    if anime_id.isdigit() and int(anime_id)+1 <= len(anime_list):

        anime_file = animes_list[anime_list[int(anime_id)]]

        anime_choice[cid] = anime_file # Hold the chosen file for the next step!
        
        anime_dict = load_dict(str(anime_file))
        
        episodes_list = list() # Create a list of keys that are integers from the anime_dict.
        
        for episode in anime_dict:
            if isinstance(episode, int):
                episodes_list.append(episode)
        
        episodes_list.sort()
        
        bot.send_photo(message.chat.id, anime_dict['Poster'])
        
        emoticom = '🔹'

        reply_msg = emoticom + '<b>Description:</b>\n'
        reply_msg += anime_dict['Description'] + '\n'
        reply_msg += emoticom + '<b>Genre:</b>\n'
        reply_msg += anime_dict['Genre'] + '\n'
        reply_msg += emoticom + '<b>Episodes Available:</b>\n'
        for episode in episodes_list:
            reply_msg += '/' + str(episode) + ', '
            
        reply_msg += '\nReturn to list: /animes or /close to exit.'
        bot.send_message(message.chat.id, reply_msg, parse_mode='HTML')

    else:
        users_steps[cid] = 0
        #bot.reply_to(message, 'Anime menu deactivated.')

@bot.message_handler(func=lambda message: get_user_step(get_user_id(message)) == 'reply_anime_episode_download')
def reply_anime_episode_download(message):
    cid = get_user_id(message)
    
    anime_id = message.text[1:]
    
    if '@AndreasBOT' in anime_id:
        anime_id = anime_id.strip('@AndreasBOT')

    anime_dict = load_dict(anime_choice[cid])
        
    if anime_id.isdigit() and int(anime_id) in anime_dict:
        bot.send_document(message.chat.id, anime_dict[int(anime_id)])

    else:
        users_steps[cid] = 0
        bot.reply_to(message, 'Anime menu deactivated.')

### Anime editor ###
@bot.message_handler(commands=['edit'])
def reply_anime_editor(message):
    cid = get_user_id(message)
    if cid in admin_users:
        users_steps[cid] = 'edit_mode'
        reply_anime_list(message)

def editor_get_anime_id(message):
    cid = get_user_id(message)
    
    anime_id = message.text[1:]
    
    anime_list = sorted(list(animes_list))
    
    if anime_id.isdigit() and int(anime_id)+1 <= len(anime_list):
        anime_file = animes_list[anime_list[int(anime_id)]]

        anime_choice[cid] = anime_file #Hold the chosen file for the next step!
        
        bot.reply_to(message, 'Send a picture for the poster.')
        
        users_steps[cid] = 'editor_get_poster'
        
    else:
        bot.reply_to(message, 'Operation canceled!')
        users_steps[cid] = 0
        
@bot.message_handler(func=lambda message: get_user_step(get_user_id(message)) == 'editor_get_poster', content_types=['photo'])
def editor_get_poster(message):
    cid = get_user_id(message)
    
    if cid in users_steps and users_steps[cid] == 'editor_get_poster':
        
        anime_dict = load_dict(anime_choice[cid])
        anime_dict['Poster'] = message.photo[-1].file_id
        save_dict(anime_choice[cid], anime_dict)

        markup = types.ForceReply(selective=True)
        msg = bot.reply_to(message, 'Now, write the serie\'s description.', reply_markup=markup)
        users_steps[cid] = ''
        bot.register_next_step_handler(msg, editor_anime_description)
        
def editor_anime_description(message):
    cid = get_user_id(message)
    
    text = message.text
    
    if text == '/cancel':
        bot.reply_to(message, 'Operation canceled!')
        users_steps[cid] = 0
        return
    
    anime_dict = load_dict(anime_choice[cid])
    anime_dict['Description'] = text
    save_dict(anime_choice[cid], anime_dict)
    
    markup = types.ForceReply(selective=True)
    msg = bot.reply_to(message, 'Finally, write the genre.', reply_markup=markup)
    
    bot.register_next_step_handler(msg, editor_anime_genre)
    
def editor_anime_genre(message):
    cid = get_user_id(message)
    
    text = message.text
    
    if text == '/cancel':
        bot.reply_to(message, 'Operation canceled!')
        users_steps[cid] = 0
        return
    
    anime_dict = load_dict(anime_choice[cid])
    anime_dict['Genre'] = text
    
    save_dict(anime_choice[cid], anime_dict)
    
    bot.send_message(message.chat.id, 'Changes saved sucessfully.')

### File Manager ###
@bot.message_handler(func=lambda message: get_file_extention(message) == '.mp4', content_types=['document'])
def receive_new_anime_episode(message):
    # handling with: "message.document.mime_type == 'video/mp4'" will crash python (Can't fix)
    #if a file is named 'Cool.file.name.mp4', it won't be accepted. (Needless to adress such cenario)
    
    if message.document.mime_type != 'video/mp4':
        return
        
    if message.document.file_name.endswith('.gif.mp4'): # FIXED: gifs now end with .mp4
        return

    cid = get_user_id(message)
    
    file_name = message.document.file_name[:-4] # split('.mp4') may cut a '.' somewhere else. so we juts cut 4 chars at the end.

    if cid in admin_users:
        new_anime_id[cid] = message.document.file_id
        # Future: Check one file format, then another, then if both fail, return false.
        is_in_format, name, episode = check_file_name_format2(file_name)
        
        if is_in_format:
            if name in animes_list:
                new_anime_ep = load_dict('files/animes/' + str(name) + '.txt')
                add_key_dict('files/animes/' + str(name) + '.txt', new_anime_ep, episode, new_anime_id[cid])
                bot.reply_to(message, 'Serie exists, episode (re)added.')
                
            else:
                new_anime_ep = create_new_anime_dict(name)
                add_key_dict('files/animes/' + str(name) + '.txt', new_anime_ep, episode, new_anime_id[cid])
                bot.reply_to(message, 'New serie, first episode added!')
        else:
            markup = types.ForceReply(selective=True)
            msg = bot.reply_to(message, 'What is the serie\'s name?\nWrite how it will be listed!\n/cancel to stop the operation!', reply_markup=markup)

            bot.register_next_step_handler(msg, choose_anime_name)

def create_new_anime_dict(anime_name):
    new_path = 'files/animes/' + str(anime_name) + '.txt'
    add_key_dict(animes_list_file, animes_list, anime_name, new_path)

    new_dict = create_dict(new_path)
    new_dict['Poster'] = 'AgADAQADmbExGzCXsAFoBUIdRnssuIEE2ykABEp6LoW_dAvwHPwAAgI'
    new_dict['Description'] = 'Nothing yet.'
    new_dict['Genre'] = 'None yet.'
    save_dict(new_path, new_dict)
    return new_dict
    
def check_file_name_format(file_name):
    'Example file (1)'
    if file_name[-1] == ')' and file_name.find(' ('):
        start = file_name.find('(') + 1
        end = len(file_name) - 1
        name = file_name[:start-2]
        
        if file_name[start:end].isdigit():
            return True, name, int(file_name[start:end]) # Save episode number as int!

    else:
        #check_file_name_format2(file_name)
        return False, 0, 0
    
def check_file_name_format2(file_name):
    'Example file 01, Example file 2'
    if file_name.split(' ')[-1].isdigit():
    
        start = file_name.find(file_name.split(' ')[-1])
        end = len(file_name)
        name = file_name[:start - 1]
        
        if file_name[start] == '0':
            start += 1

        return True, name, int(file_name[start:end]) # Save episode number as int!

    else:
        return False, 0, 0

def choose_anime_name(message):
    cid = get_user_id(message)
    
    name = message.text
    new_anime_name[cid] = name

    markup = types.ForceReply(selective=True)
        
    if name == '/cancel':
        bot.reply_to(message, 'Operation canceled!')
        return
        
    elif name in animes_list:
        msg = bot.reply_to(message, 'Serie exists, what episode should I link to it?', reply_markup=markup)
        bot.register_next_step_handler(msg, choose_anime_episode)
    
    else:
        create_new_anime_dict(name)
        msg = bot.reply_to(message, 'New serie! What episode should I link to it?', reply_markup=markup)
        bot.register_next_step_handler(msg, choose_anime_episode)

def choose_anime_episode(message):
    cid = get_user_id(message)
    episode = message.text

    if episode.isdigit():
        new_anime_ep = load_dict('files/animes/' + str(new_anime_name[cid]) + '.txt')
        add_key_dict('files/animes/' + str(new_anime_name[cid]) + '.txt', new_anime_ep, episode, new_anime_id[cid])
        bot.reply_to(message, 'Serie (now) exists and the episode has been (re)added!')

    else:
        bot.reply_to(message, 'Operation canceled!')
        return
        
        
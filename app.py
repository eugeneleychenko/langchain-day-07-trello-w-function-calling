import requests
import streamlit as st
import os
from dotenv import find_dotenv, load_dotenv

API_KEY = os.getenv("API_KEY")
TOKEN = os.getenv("TOKEN")
AUTH_PARAMS = {'key': API_KEY, 'token': TOKEN}



def get_boards():
    url = "https://api.trello.com/1/members/me/boards"
    response = requests.get(url, params=AUTH_PARAMS)
    return response.json()

# Function to get lists of a board
def get_lists(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    response = requests.get(url, params=AUTH_PARAMS)
    return response.json()

# Function to get cards of a board
def get_cards(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    response = requests.get(url, params=AUTH_PARAMS)
    return response.json()

# Function to add a member to a card
def add_member_to_card(card_id, member_id):
    url = f"https://api.trello.com/1/cards/{card_id}/idMembers"
    query = {
        'value': member_id,
        **AUTH_PARAMS
    }
    response = requests.post(url, params=query)
    return response.json()

def create_card(board_id, list_id, card_name):
    url = f"https://api.trello.com/1/cards"
    query = {
        'idList': list_id,
        'name': card_name,
        **AUTH_PARAMS
    }
    response = requests.post(url, params=query)
    return response.json()

def modify_card(card_id, new_name):
    url = f"https://api.trello.com/1/cards/{card_id}"
    query = {
        'name': new_name,
        **AUTH_PARAMS
    }
    response = requests.put(url, params=query)
    return response.json()


def get_members(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/members"
    response = requests.get(url, params=AUTH_PARAMS)
    return response.json()

def add_member(board_id, member_id):
    url = f"https://api.trello.com/1/boards/{board_id}/members/{member_id}"
    query = {
        'type': 'normal',
        **AUTH_PARAMS
    }
    response = requests.put(url, params=query)
    return response.json()
def move_card(card_id, new_list_id):
    url = f"https://api.trello.com/1/cards/{card_id}"
    query = {
        'idList': new_list_id,
        **AUTH_PARAMS
    }
    response = requests.put(url, params=query)
    return response.json()

def add_description(card_id, description):
    url = f"https://api.trello.com/1/cards/{card_id}"
    query = {
        'desc': description,
        **AUTH_PARAMS
    }
    response = requests.put(url, params=query)
    return response.json()

def add_comment(card_id, comment):
    url = f"https://api.trello.com/1/cards/{card_id}/actions/comments"
    query = {
        'text': comment,
        **AUTH_PARAMS
    }
    response = requests.post(url, params=query)
    return response.json()

def main():
    load_dotenv(find_dotenv())
    boards = get_boards()
    if not boards:
        st.error('No boards found.')
    else:
        board_names = [board['name'] for board in boards]
        selected_board_name = st.selectbox('Select a board', board_names)

        # Get the selected board id
        selected_board_id = [board['id'] for board in boards if board['name'] == selected_board_name][0]

        # Get the lists and cards of the selected board
        lists = get_lists(selected_board_id)
        cards = get_cards(selected_board_id)
        # Choose an action
        action = st.selectbox('Choose an action', ['Create a card', 'Modify a card', 'Move a card', 'Add a description', 'Add a comment', 'List members', 'Add a member'])


    if action == 'Create a card':
        list_names = [list['name'] for list in lists]
        selected_list_name = st.selectbox('Select a list', list_names)
        card_name = st.text_input('Enter card name')
        if st.button('Create card'):
            selected_list_id = [list['id'] for list in lists if list['name'] == selected_list_name][0]
            create_card(selected_board_id, selected_list_id, card_name)
            st.write('Card created.')

    elif action == 'Modify a card':
        card_names = [card['name'] for card in cards]
        selected_card_name = st.selectbox('Select a card', card_names)
        new_name = st.text_input('Enter new name')
        if st.button('Modify card'):
            selected_card_id = [card['id'] for card in cards if card['name'] == selected_card_name][0]
            modify_card(selected_card_id, new_name)
            st.write('Card modified.')

    elif action == 'Move a card':
        card_names = [card['name'] for card in cards]
        selected_card_name = st.selectbox('Select a card', card_names)
        list_names = [list['name'] for list in lists]
        selected_list_name = st.selectbox('Select a list', list_names)
        if st.button('Move card'):
            selected_card_id = [card['id'] for card in cards if card['name'] == selected_card_name][0]
            selected_list_id = [list['id'] for list in lists if list['name'] == selected_list_name][0]
            move_card(selected_card_id, selected_list_id)
            st.write('Card moved.')

    elif action == 'Add a description':
        card_names = [card['name'] for card in cards]
        selected_card_name = st.selectbox('Select a card', card_names)
        description = st.text_input('Enter description')
        if st.button('Add description'):
            selected_card_id = [card['id'] for card in cards if card['name'] == selected_card_name][0]
            add_description(selected_card_id, description)
            st.write('Description added.')

    elif action == 'Add a comment':
        card_names = [card['name'] for card in cards]
        selected_card_name = st.selectbox('Select a card', card_names)
        comment = st.text_input('Enter comment')
        if st.button('Add comment'):
            selected_card_id = [card['id'] for card in cards if card['name'] == selected_card_name][0]
            add_comment(selected_card_id, comment)
            st.write('Comment added.')

    elif action == 'List members':
        members = get_members(selected_board_id)
        member_names = [member['fullName'] for member in members]
        st.write('Members:', ', '.join(member_names))

    elif action == 'Add a member':
        members = get_members(selected_board_id)
        member_names = [member['fullName'] for member in members]
        selected_member_name = st.selectbox('Select a member', member_names)
        card_names = [card['name'] for card in cards]
        selected_card_name = st.selectbox('Select a card', card_names)
        if st.button('Add member'):
            selected_member_id = [member['id'] for member in members if member['fullName'] == selected_member_name][0]
            selected_card_id = [card['id'] for card in cards if card['name'] == selected_card_name][0]
            add_member_to_card(selected_card_id, selected_member_id)
            st.write('Member added.')

if __name__ == '__main__':
    main()
import os
from trello import TrelloClient
import streamlit as st
from dotenv import find_dotenv, load_dotenv

API_KEY = os.getenv("API_KEY")
TOKEN = os.getenv("TOKEN")

client = TrelloClient(
    api_key=API_KEY,
    api_secret=None,
    token=TOKEN,
    token_secret=None
)

def get_boards():
    return client.list_boards()

def get_lists(board):
    return board.list_lists()

def get_cards(list):
    return list.list_cards()

def create_card(list, card_name):
    return list.add_card(card_name)

def modify_card(card, new_name):
    return card.set_name(new_name)

def move_card(card, new_list):
    return card.change_list(new_list.id)

def add_description(card, description):
    return card.set_description(description)

def add_comment(card, comment):
    return card.comment(comment)

def get_members(board):
    return board.get_members()

def add_member(card, member_id):
    return card.add_member(member_id)

def main():
    load_dotenv(find_dotenv())
    
    st.header("Control Your Trello")
    
    boards = get_boards()
    
    if not boards:
        st.error('No boards found.')
    else:
        board_names = [board.name for board in boards]
        selected_board_name = st.selectbox('Select a board', board_names)

        # Get the selected board
        selected_board = [board for board in boards if board.name == selected_board_name][0]

        # Get the lists and cards of the selected board
        lists = get_lists(selected_board)
        cards = [card for list in lists for card in get_cards(list)]
        # Choose an action
        action = st.selectbox('Choose an action', ['Create a card', 'Modify a card', 'Move a card', 'Add a description', 'Add a comment', 'List members', 'Add a member'])

        if action == 'Create a card':
            list_names = [list.name for list in lists]
            selected_list_name = st.selectbox('Select a list', list_names)
            card_name = st.text_input('Enter card name')
            if st.button('Create card'):
                selected_list = [list for list in lists if list.name == selected_list_name][0]
                create_card(selected_list, card_name)
                st.write('Card created.')

        elif action == 'Modify a card':
            card_names = [card.name for card in cards]
            selected_card_name = st.selectbox('Select a card', card_names)
            new_name = st.text_input('Enter new name')
            if st.button('Modify card'):
                selected_card = [card for card in cards if card.name == selected_card_name][0]
                modify_card(selected_card, new_name)
                st.write('Card modified.')

        elif action == 'Move a card':
            card_names = [card.name for card in cards]
            selected_card_name = st.selectbox('Select a card', card_names)
            list_names = [list.name for list in lists]
            selected_list_name = st.selectbox('Select a list', list_names)
            if st.button('Move card'):
                selected_card = [card for card in cards if card.name == selected_card_name][0]
                selected_list = [list for list in lists if list.name == selected_list_name][0]
                move_card(selected_card, selected_list)
                st.write('Card moved.')

        elif action == 'Add a description':
            card_names = [card.name for card in cards]
            selected_card_name = st.selectbox('Select a card', card_names)
            description = st.text_input('Enter description')
            if st.button('Add description'):
                selected_card = [card for card in cards if card.name == selected_card_name][0]
                add_description(selected_card, description)
                st.write('Description added.')

        elif action == 'Add a comment':
            card_names = [card.name for card in cards]
            selected_card_name = st.selectbox('Select a card', card_names)
            comment = st.text_input('Enter comment')
            if st.button('Add comment'):
                selected_card = [card for card in cards if card.name == selected_card_name][0]
                add_comment(selected_card, comment)
                st.write('Comment added.')

        elif action == 'List members':
            members = get_members(selected_board)
            member_names = [member.full_name for member in members]
            st.write('Members:', ', '.join(member_names))

        elif action == 'Add a member':
            members = get_members(selected_board)
            member_names = [member.full_name for member in members]
            selected_member_name = st.selectbox('Select a member', member_names)
            card_names = [card.name for card in cards]
            selected_card_name = st.selectbox('Select a card', card_names)
            if st.button('Add member'):
                selected_member_id = [member.id for member in members if member.full_name == selected_member_name][0]
                selected_card = [card for card in cards if card.name == selected_card_name][0]
                add_member(selected_card, selected_member_id)
                st.write('Member added.')
                   

if __name__ == '__main__':
    main()
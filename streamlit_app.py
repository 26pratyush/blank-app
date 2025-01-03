import streamlit as st

# Encryption and Decryption Functions
def shift_char(c, shift):
    if 'a' <= c <= 'z':
        return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
    elif 'A' <= c <= 'Z':
        return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
    else:
        return c

def custom_encrypt(text):
    space_positions = [i for i, char in enumerate(text) if char == ' ']
    text = text.replace(" ", "")
    result = []
    pairs = [text[i:i+2] for i in range(0, len(text), 2)]
    
    for i, pair in enumerate(pairs):
        if len(pair) == 2:
            swapped = pair[1] + pair[0]
            for j, char in enumerate(swapped):
                new_position = 2 * i + j
                if new_position % 2 == 0:
                    result.append(shift_char(char, 1))
                else:
                    result.append(shift_char(char, -1))
        else:
            last_char = pair[0]
            new_position = 2 * i
            if new_position % 2 == 0:
                result.append(shift_char(last_char, 1))
            else:
                result.append(shift_char(last_char, -1))

    encrypted_text = ''.join(result)
    return encrypted_text, space_positions

def custom_decrypt(encrypted_text, space_positions):
    result = []
    pairs = [encrypted_text[i:i+2] for i in range(0, len(encrypted_text), 2)]
    
    for i, pair in enumerate(pairs):
        if len(pair) == 2:
            adjusted_pair = ""
            for j, char in enumerate(pair):
                new_position = 2 * i + j
                if new_position % 2 == 0:
                    adjusted_pair += shift_char(char, -1)
                else:
                    adjusted_pair += shift_char(char, 1)
            result.append(adjusted_pair[1] + adjusted_pair[0])
        else:
            last_char = pair[0]
            new_position = 2 * i
            if new_position % 2 == 0:
                result.append(shift_char(last_char, -1))
            else:
                result.append(shift_char(last_char, 1))

    decrypted_text = ''.join(result)
    for pos in space_positions:
        decrypted_text = decrypted_text[:pos] + ' ' + decrypted_text[pos:]

    return decrypted_text

# Streamlit App
st.set_page_config(page_title="Swap & Step Encryption", layout="centered", initial_sidebar_state="collapsed")

st.title("🔒 Swap & Step Encryption")
st.markdown("Welcome to the **Swap & Step Encryption** app! Start by encrypting your plaintext.")

# Navigation
pages = ["Welcome", "Encrypt", "Decrypt"]
selected_page = st.sidebar.radio("Navigate", pages)

if selected_page == "Welcome":
    st.header("Welcome")
    st.write("Click the 'Encrypt' tab in the sidebar to begin the encryption process.")

elif selected_page == "Encrypt":
    st.header("Encrypt Your Text")
    plaintext = st.text_input("Enter plaintext:")
    encrypt_button = st.button("Tap to Encrypt")
    
    if encrypt_button and plaintext:
        encrypted_text, space_positions = custom_encrypt(plaintext)
        st.write(f"**Encrypted Text:** {encrypted_text}")
        st.session_state["encrypted_text"] = encrypted_text
        st.session_state["space_positions"] = space_positions

elif selected_page == "Decrypt":
    st.header("Decrypt Your Text")
    
    if "encrypted_text" in st.session_state and "space_positions" in st.session_state:
        encrypted_text = st.session_state["encrypted_text"]
        space_positions = st.session_state["space_positions"]
        st.write(f"**Encrypted Text:** {encrypted_text}")
        
        decrypt_button = st.button("Tap to Decrypt")
        if decrypt_button:
            decrypted_text = custom_decrypt(encrypted_text, space_positions)
            st.write(f"**Decrypted Text:** {decrypted_text}")
    else:
        st.warning("No encrypted text available. Please encrypt some text first!")

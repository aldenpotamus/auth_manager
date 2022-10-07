from auth_manager import AuthManager
import configparser

def main():
    youtube = AuthManager.get_authenticated_service(CONFIG['TEST'], 
                                                    authConfig=CONFIG['AUTH_MANAGER'])
                                
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        myRating="like"
    )
    response = request.execute()

    print(response)

if __name__ == '__main__':
    print('Parsing config file...')
    CONFIG = configparser.ConfigParser()
    CONFIG.read('config.ini')   

    main()
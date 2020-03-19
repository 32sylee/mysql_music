import pymysql as pms


def intro():
    """
    0. 첫화면
    """
    print('\n음악 어플리케이션에 오신 것을 환영합니다!!')
    print('0. 나가기')
    print('1. 관리자메뉴')
    print('2. 사용자메뉴')
    while 1:
        print('입력:', end=' ')
        input_no = input()
        if input_no == '0':
            return -1
        elif input_no == '1':
            return 15
        elif input_no == '2':
            return 1
        else:
            print('잘못 입력하셨습니다. 다시 입력하세요')


def user_menu():
    """
    1. 사용자메뉴
    """
    print('\n사용자메뉴입니다.')
    print('0. 이전화면으로')
    print('1. 로그인')
    print('2. 회원가입')
    while 1:
        print('입력:', end=' ')
        input_no = input()
        if input_no == '0':
            return 0
        elif input_no == '1':
            return 2
        elif input_no == '2':
            return 7
        else:
            print('잘못 입력하셨습니다. 다시 입력하세요')


def login():
    """
    2. 로그인
    """
    connection = pms.connect(
        host='localhost',
        port=3306,
        user='db',
        password='db!',
        db='music',
        charset='utf8')

    try:
        with connection.cursor(pms.cursors.DictCursor) as cursor:
            sql = "SELECT user_no, user_id, user_pw, user_name FROM user WHERE user_id = %s AND user_pw = %s;"

            while 1:
                print('\n사용자 로그인')
                print('아이디를 입력하세요:', end=' ')
                id = input()
                print('비밀번호를 입력하세요:', end=' ')
                pw = input()

                a = cursor.execute(sql, (id, pw))
                result = cursor.fetchone()

                connection.commit()

                if a == 1:  # 로그인 성공
                    global user_no
                    user_no = int(result['user_no'])
                    user_name = result['user_name']
                    print('\n' + user_name + '님 환영합니다!')
                    return 3
                else:
                    print('\n아이디나 비밀번호가 틀립니다.')
                    print('0. 이전화면')
                    print('1. 다시 로그인')
                    print('입력:', end=' ')
                    input_no = input()
                    while 1:
                        if input_no == '0':
                            return 1
                        elif input_no == '1':
                            break
                        else:
                            print('잘못 입력하셨습니다. 다시 입력하세요')
    finally:
        connection.close()


def user_main():
    """
    3. 사용자메인
    """
    print('\n사용자 메인페이지입니다.')
    print('0. 로그아웃')
    print('1. 내 플레이리스트 보기')
    print('2. 음악 검색')
    print('3. 아티스트 검색')
    print('4. 장르별 음악')
    while 1:
        print('입력:', end=' ')
        input_no = input()
        if input_no == '0':
            global user_no
            user_no = -1
            return 1
        elif input_no == '1':
            return 4
        elif input_no == '2':
            print('\n검색하실 음악 제목을 입력하세요:', end=' ')
            global input_title
            input_title = input()
            input_title = '%' + input_title + '%'
            return 6
        elif input_no == '3':
            print('\n검색하실 아티스트명을 입력하세요:', end=' ')
            global input_artist
            input_artist = input()
            input_artist = '%' + input_artist + '%'
            return 8
        elif input_no == '4':
            return 9
        else:
            print('잘못 입력하셨습니다. 다시 입력하세요')


def playlist():
    """
    4. 내 플레이리스트 보기
    """
    connection = pms.connect(
        host='localhost',
        port=3306,
        user='db',
        password='db!',
        db='music',
        charset='utf8')

    try:
        with connection.cursor(pms.cursors.DictCursor) as cursor:
            sql = """SELECT S.song_no, S.song_title, S.artist_list
                    FROM song_list S, playlist P
                    WHERE S.song_no = P.song_no AND P.user_no = %s;"""
            global user_no
            cursor.execute(sql, user_no)
            result = cursor.fetchall()
            connection.commit()
            print('\n내 플레이리스트 보기')
            print('-----------------------------------------------------------------------')
            print('번호\t\t음악제목\t\t\t\t\t아티스트')
            print('-----------------------------------------------------------------------')

            for row in result:
                print(str(row['song_no']) + '\t\t' + row['song_title'] + '\t\t\t\t\t' + row['artist_list'])

            print('-----------------------------------------------------------------------')

    finally:
        connection.close()

    print('0. 이전화면')
    print('1. 플레이리스트 삭제')

    while 1:
        print('입력:', end=' ')
        input_no = input()
        if input_no == '0':
            return 3
        elif input_no == '1':
            return 5
        else:
            print('잘못 입력하셨습니다. 다시 입력하세요')


def delete_playlist():
    """
    5. 플레이리스트 삭제
    """
    while 1:
        connection = pms.connect(
            host='localhost',
            port=3306,
            user='db',
            password='db!',
            db='music',
            charset='utf8')

        print('\n삭제하실 음악번호를 입력하세요:', end=' ')
        input_no = input()

        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM playlist WHERE user_no = %s AND song_no = %s;"
                a = cursor.execute(sql, (user_no, input_no))

                connection.commit()
        finally:
            connection.close()

        if a == 1:
            print('\n삭제되었습니다.')
            return 4
        else:
            print('잘못 입력하셨습니다.')


def search_song():
    """
    6. 음악 검색
    """
    connection = pms.connect(
        host='localhost',
        port=3306,
        user='db',
        password='db!',
        db='music',
        charset='utf8')

    try:
        with connection.cursor(pms.cursors.DictCursor) as cursor:
            sql = """SELECT song_no, song_title, artist_list
                    FROM song_list
                    WHERE song_title LIKE %s;"""
            cursor.execute(sql, input_title)
            result = cursor.fetchall()
            connection.commit()
            print('\n검색 결과')
            print('-----------------------------------------------------------------------')
            print('번호\t\t음악제목\t\t\t\t\t아티스트')
            print('-----------------------------------------------------------------------')

            for row in result:
                print(str(row['song_no']) + '\t\t' + row['song_title'] + '\t\t\t\t\t\t' + row['artist_list'])

            print('-----------------------------------------------------------------------')

    finally:
        connection.close()

    while 1:
        print('0. 이전화면')
        print('1. 플레이리스트 등록')
        print('2. 앨범 정보 보기')
        print('입력:', end=' ')

        input_no = input()
        if input_no == '0':
            return 3
        elif input_no == '1':
            return 10
        elif input_no == '2':
            return 11
        else:
            print('잘못 입력하셨습니다. 다시 입력하세요')


def join():
    """
    7. 회원가입
    """
    print('\n회원가입 정보를 입력하세요.')
    print('아이디:', end=' ')
    id = input()
    print('비밀번호:', end=' ')
    pw = input()
    print('이름:', end=' ')
    name = input()
    print('생년월일(ex. 2001-01-01):', end=' ')
    birth = input()
    print('이메일:', end=' ')
    email = input()

    connection = pms.connect(
        host='localhost',
        port=3306,
        user='db',
        password='db!',
        db='music',
        charset='utf8')

    try:
        with connection.cursor() as cursor:
            sql = "SELECT MAX(user_no) FROM user;"
            a = cursor.execute(sql)
            if a == 0:
                no = 0
            else:
                result = cursor.fetchone()
                no = result[0] + 1
            connection.commit()

        with connection.cursor() as cursor:
            sql = "INSERT INTO user VALUES(%s, %s, %s, %s, %s, %s);"

            cursor.execute(sql, (no, id, pw, name, birth, email))
            connection.commit()

            print('\n회원가입이 완료되었습니다.')

    except pms.err.IntegrityError:
        print('\n이미 존재하는 아이디입니다')
    except pms.err.InternalError:
        print("\n생년월일은 'YYYY-MM-DD' 형식으로 입력해주세요")

    finally:
        connection.close()

    return 1


def search_artist():
    """
    8. 아티스트 검색
    """
    connection = pms.connect(
        host='localhost',
        port=3306,
        user='db',
        password='db!',
        db='music',
        charset='utf8')

    try:
        with connection.cursor(pms.cursors.DictCursor) as cursor:
            sql = """SELECT artist_no, artist_name, type, more_info
                    FROM artist_list
                    WHERE artist_name LIKE %s;"""
            cursor.execute(sql, input_artist)
            result = cursor.fetchall()
            connection.commit()
            print('\n검색 결과')
            print('-------------------------------------------')
            print('번호\t\t아티스트명')
            print('-------------------------------------------')

            for row in result:
                if row['type'] == '솔로' and row['more_info'] is not None:
                    print(str(row['artist_no']) + '\t\t' + row['artist_name'] + '(' + row['more_info'] + ')')
                else:
                    print(str(row['artist_no']) + '\t\t' + row['artist_name'])

            print('-------------------------------------------')

    finally:
        connection.close()

    while 1:
        print('0. 이전화면')
        print('1. 아티스트 정보 보기')
        print('입력:', end=' ')

        input_no = input()
        if input_no == '0':
            return 3
        elif input_no == '1':
            return 12
        else:
            print('잘못 입력하셨습니다. 다시 입력하세요')


def search_genre():
    """
    9. 장르별 음악
    """
    print('\n1. 발라드')
    print('2. 댄스')
    print('3. 힙합')
    print('4. 록')
    print('5. 포크')
    print('6. 트로트')
    print('7. POP')

    while 1:
        print('원하시는 장르를 입력하세요:', end=' ')
        input_no = input()
        if input_no == '1':
            input_genre = '발라드'
            break
        elif input_no == '2':
            input_genre = '댄스'
            break
        elif input_no == '3':
            input_genre = '힙합'
            break
        elif input_no == '4':
            input_genre = '록'
            break
        elif input_no == '5':
            input_genre = '포크'
            break
        elif input_no == '6':
            input_genre = '트로트'
            break
        elif input_no == '7':
            input_genre = 'POP'
            break
        else:
            print('잘못 입력하셨습니다.')

    connection = pms.connect(
        host='localhost',
        port=3306,
        user='db',
        password='db!',
        db='music',
        charset='utf8')

    try:
        with connection.cursor(pms.cursors.DictCursor) as cursor:
            sql = """SELECT song_no, song_title, artist_list
                    FROM song_list
                    WHERE genre = %s;"""
            cursor.execute(sql, input_genre)
            result = cursor.fetchall()
            connection.commit()
            print('\n검색 결과')
            print('-----------------------------------------------------------------------')
            print('번호\t\t음악제목\t\t\t\t\t아티스트')
            print('-----------------------------------------------------------------------')

            for row in result:
                print(str(row['song_no']) + '\t\t' + row['song_title'] + '\t\t\t\t\t\t' + row['artist_list'])

            print('-----------------------------------------------------------------------')

    finally:
        connection.close()

    while 1:
        print('0. 이전화면')
        print('1. 플레이리스트 등록')
        print('2. 앨범 정보 보기')
        print('입력:', end=' ')

        input_no = input()
        if input_no == '0':
            return 3
        elif input_no == '1':
            return 10
        elif input_no == '2':
            return 11
        else:
            print('잘못 입력하셨습니다. 다시 입력하세요')


def insert_playlist():
    """
    10. 플레이리스트 등록
    """
    while 1:
        connection = pms.connect(
            host='localhost',
            port=3306,
            user='db',
            password='db!',
            db='music',
            charset='utf8')

        print('\n등록하실 음악번호를 입력하세요:', end=' ')
        input_no = input()

        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO playlist VALUES(%s, %s);"
                global user_no
                try:
                    a = cursor.execute(sql, (user_no, input_no))
                    connection.commit()
                except pms.err.IntegrityError:
                    a = 0
        finally:
            connection.close()

        if a == 1:
            print('\n등록되었습니다.')
            return 3
        else:
            print('이미 등록된 음악이거나 잘못 입력하셨습니다.')
            return 3


def album_info():
    """
    11. 앨범 정보 보기
    """
    while 1:
        connection = pms.connect(
            host='localhost',
            port=3306,
            user='db',
            password='db!',
            db='music',
            charset='utf8')

        print('음악번호를 입력하세요:', end=' ')
        input_no = input()

        try:
            with connection.cursor(pms.cursors.DictCursor) as cursor:
                sql = """SELECT A.album_no, A.album_title, A.date_of_issue, A.artist_list
                        FROM song S, album_list A
                        WHERE S.album_no = A.album_no AND S.Song_no = %s;"""
                a = cursor.execute(sql, input_no)
                result = cursor.fetchone()
                connection.commit()
        finally:
            connection.close()

        if a == 1:
            album_no = result['album_no']
            print('\n앨범명: ' + result['album_title'])
            print('아티스트: ' + result['artist_list'])
            print('발매일: ' + result['date_of_issue'].strftime('%Y-%m-%d'))

            connection = pms.connect(
                host='localhost',
                port=3306,
                user='db',
                password='db!',
                db='music',
                charset='utf8')

            try:
                with connection.cursor(pms.cursors.DictCursor) as cursor:
                    sql = """SELECT SL.song_no, SL.song_title, SL.artist_list
                            FROM song S, song_list SL
                            WHERE S.song_no = SL.song_no AND S.album_no = %s;"""
                    cursor.execute(sql, album_no)
                    result = cursor.fetchall()
                    connection.commit()
            finally:
                connection.close()

            print('-----------------------------------------------------------------------')
            print('번호\t\t음악제목\t\t\t\t\t아티스트')
            print('-----------------------------------------------------------------------')
            for row in result:
                print(str(row['song_no']) + '\t\t' + row['song_title'] + '\t\t\t\t\t\t' + row['artist_list'])
            print('-----------------------------------------------------------------------')
            print('이전화면으로 돌아가시려면 아무 키나 입력해주세요:', end=' ')
            input()
            return 6
        else:
            print('잘못 입력하셨습니다.')


def artist_info():
    """
    12. 아티스트 정보 보기
    """
    while 1:
        connection = pms.connect(
            host='localhost',
            port=3306,
            user='db',
            password='db!',
            db='music',
            charset='utf8')

        global artist_no
        if artist_no == -1:
            print('아티스트번호를 입력하세요:', end=' ')
            artist_no = input()

        try:
            with connection.cursor(pms.cursors.DictCursor) as cursor:
                sql = """SELECT *
                        FROM artist_list
                        WHERE artist_no = %s;"""
                a = cursor.execute(sql, artist_no)
                result = cursor.fetchone()
                connection.commit()
        finally:
            connection.close()

        if a == 1:
            print('\n------------------------------------')
            print('아티스트명: ' + result['artist_name'])
            print('데뷔년도: ' + str(result['debut_year']) + '년')
            print('국적: ' + result['nationality'])
            print('유형: ' + result['type'])
            if result['type'] == '그룹':
                print('멤버: ' + result['more_info'])
            elif result['type'] == '솔로' and result['more_info'] is not None:
                print('소속그룹: ' + result['more_info'])
            print('------------------------------------')

            print('0. 이전화면')
            print('1. 참여 앨범 보기')
            print('2. 참여 음악 보기')

            while 1:
                print('입력:', end=' ')
                input_no = input()
                if input_no == '0':
                    artist_no = -1
                    return 3
                elif input_no == '1':
                    return 13
                elif input_no == '2':
                    return 14
                else:
                    print('잘못 입력하셨습니다. 다시 입력하세요')

        else:
            print('잘못 입력하셨습니다.')


def artist_info_album():
    """
    13. 아티스트 앨범 정보 보기
    """
    while 1:
        connection = pms.connect(
            host='localhost',
            port=3306,
            user='db',
            password='db!',
            db='music',
            charset='utf8')

        global artist_no

        try:
            with connection.cursor(pms.cursors.DictCursor) as cursor:
                sql = """(SELECT A.album_no, A.album_title, A.date_of_issue, A.artist_list
                        FROM album_list A, participate_album PA, belong_to B
                        WHERE A.album_no = PA.album_no AND PA.artist_no = B.group_no AND B.member_no = %s)
                        UNION
                        (SELECT A.album_no, A.album_title, A.date_of_issue, A.artist_list
                        FROM album_list A, participate_album PA
                        WHERE A.album_no = PA.album_no AND PA.artist_no = %s);"""
                cursor.execute(sql, (artist_no, artist_no))
                result = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()

        print('--------------------------------------------------------------------------')
        print('번호\t\t앨범제목\t\t\t\t\t\t아티스트\t\t\t\t\t발매일')
        print('--------------------------------------------------------------------------')
        for row in result:
            print(
                str(row['album_no']) + '\t\t' + row['album_title'] + '\t\t' + row['artist_list'] + '\t\t' +
                row['date_of_issue'].strftime('%Y-%m-%d'))
        print('--------------------------------------------------------------------------')
        print('이전화면으로 돌아가시려면 아무 키나 입력해주세요:', end=' ')
        input()
        return 12


def artist_info_song():
    """
    14. 아티스트 음악 정보 보기
    """
    while 1:
        connection = pms.connect(
            host='localhost',
            port=3306,
            user='db',
            password='db!',
            db='music',
            charset='utf8')

        global artist_no

        try:
            with connection.cursor(pms.cursors.DictCursor) as cursor:
                sql = """(SELECT S.song_no, S.song_title, S.artist_list
                        FROM song_list S, participate_song PS, belong_to B
                        WHERE S.song_no = PS.song_no AND PS.artist_no = B.group_no AND B.member_no = %s)
                        UNION
                        (SELECT S.song_no, S.song_title, S.artist_list
                        FROM song_list S, participate_song PS
                        WHERE S.song_no = PS.song_no AND PS.artist_no = %s);"""
                cursor.execute(sql, (artist_no, artist_no))
                result = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()

        print('-----------------------------------------------------------------------')
        print('번호\t\t음악제목\t\t\t\t\t\t아티스트')
        print('-----------------------------------------------------------------------')

        for row in result:
            print(str(row['song_no']) + '\t\t' + row['song_title'] + '\t\t\t\t' + row['artist_list'])

        print('-----------------------------------------------------------------------')
        print('이전화면으로 돌아가시려면 아무 키나 입력해주세요:', end=' ')
        input()
        return 12


def admin_menu():
    """
    15. 관리자메뉴
    """
    print('\n관리자메뉴입니다.')
    print('0. 이전화면으로')
    print('1. 로그인')
    while 1:
        print('입력:', end=' ')
        input_no = input()
        if input_no == '0':
            return 0
        elif input_no == '1':
            return 16
        else:
            print('잘못 입력하셨습니다. 다시 입력하세요')


def admin_login():
    """
    16. 관리자 로그인
    """
    connection = pms.connect(
        host='localhost',
        port=3306,
        user='db',
        password='db!',
        db='music',
        charset='utf8')

    try:
        with connection.cursor(pms.cursors.DictCursor) as cursor:
            sql = "SELECT admin_no, admin_id, admin_pw, admin_name FROM administrator WHERE admin_id = %s AND admin_pw = %s;"

            while 1:
                print('\n관리자 로그인')
                print('아이디를 입력하세요:', end=' ')
                id = input()
                print('비밀번호를 입력하세요:', end=' ')
                pw = input()

                a = cursor.execute(sql, (id, pw))
                result = cursor.fetchone()

                connection.commit()

                if a == 1:  # 로그인 성공
                    global admin_no
                    admin_no = int(result['admin_no'])
                    admin_name = result['admin_name']
                    print('\n' + admin_name + '님 환영합니다!')
                    return 17
                else:
                    print('\n아이디나 비밀번호가 틀립니다.')
                    print('0. 이전화면')
                    print('1. 다시 로그인')
                    print('입력:', end=' ')
                    input_no = input()
                    while 1:
                        if input_no == '0':
                            return 15
                        elif input_no == '1':
                            break
                        else:
                            print('잘못 입력하셨습니다. 다시 입력하세요')
    finally:
        connection.close()


def admin_main():
    """
    17. 관리자메인
    """
    print('\n관리자 메인페이지입니다.')
    print('0. 로그아웃')
    print('1. 음악 수정/삭제')
    print('2. 앨범 수정/삭제')
    print('3. 아티스트 수정/삭제')
    print('4. 음악 등록')
    print('5. 앨범 등록')
    print('6. 아티스트 등록')

    while 1:
        print('입력:', end=' ')
        input_no = input()
        if input_no == '0':
            global admin_no
            admin_no = -1
            return 15
        elif input_no == '1':
            print('\n수정/삭제하실 음악 번호를 입력하세요:', end=' ')
            global song_no
            song_no = input()
            return 18
        elif input_no == '2':
            print('\n수정/삭제하실 앨범 번호를 입력하세요:', end=' ')
            global album_no
            album_no = input()
            return 19
        elif input_no == '3':
            print('\n수정/삭제하실 아티스트 번호를 입력하세요:', end=' ')
            global artist_no
            artist_no = input()
            return 22
        elif input_no == '4':
            return 20
        elif input_no == '5':
            return 21
        elif input_no == '6':
            return 23
        else:
            print('잘못 입력하셨습니다. 다시 입력하세요')


def up_del_song():
    """
    18. 음악 수정/삭제
    """
    connection = pms.connect(
        host='localhost',
        port=3306,
        user='db',
        password='db!',
        db='music',
        charset='utf8')

    global song_no

    try:
        with connection.cursor(pms.cursors.DictCursor) as cursor:
            sql = """SELECT * FROM song_list
                    WHERE song_no = %s;"""
            cursor.execute(sql, int(song_no))
            result = cursor.fetchone()
            connection.commit()

            if result is None:
                print('잘못 입력하셨습니다.')
                return 17

            print('\n----------------------------------------')
            print('음악번호: ' + str(result['song_no']))
            print('제목: ' + result['song_title'])
            print('장르: ' + result['genre'])
            print('아티스트: ' + result['artist_list'])
            print('----------------------------------------')

    except ValueError:
        print('잘못 입력하셨습니다.')
        return 17

    finally:
        connection.close()

    print('0. 이전화면')
    print('1. 음악 정보 수정')
    print('2. 음악 삭제')

    while 1:
        print('입력:', end=' ')
        input_no = input()
        if input_no == '0':
            return 17
        elif input_no == '1':
            print('\n변경하실 정보를 선택하세요.')
            print('0. 수정 취소')
            print('1. 음악 제목')
            print('2. 음악 장르')
            print('3. 앨범')
            print('4. 아티스트')
            print('입력:', end=' ')
            input_no = input()

            connection = pms.connect(
                host='localhost',
                port=3306,
                user='db',
                password='db!',
                db='music',
                charset='utf8')
            try:
                if input_no == '0':
                    return 17
                elif input_no == '1':
                    print('\n변경될 내용을 입력해주세요:', end=' ')
                    input_update = input()
                    with connection.cursor() as cursor:
                        sql = """UPDATE song SET song_title = %s WHERE song_no = %s;"""
                        cursor.execute(sql, (input_update, song_no))
                        connection.commit()

                elif input_no == '2':
                    print('\n변경될 내용을 입력해주세요:', end=' ')
                    input_update = input()
                    if input_update not in ('발라드', '댄스', '힙합', '록', '포크', '트로트', 'POP'):
                        print("잘못 입력하셨습니다(발라드, 댄스, 힙합, 록, 포크, 트로트, POP 중에 입력해주세요)")
                        return 18
                    with connection.cursor() as cursor:
                        sql = """UPDATE song SET genre = %s WHERE song_no = %s;"""
                        cursor.execute(sql, (input_update, song_no))
                        connection.commit()

                elif input_no == '3':
                    print('\n변경될 내용을 입력해주세요:', end=' ')
                    input_update = input()
                    with connection.cursor() as cursor:
                        sql = """UPDATE song SET album_no = %s WHERE song_no = %s;"""
                        cursor.execute(sql, (input_update, song_no))
                        connection.commit()

                elif input_no == '4':
                    print('\n입력할 아티스트 수를 입력해주세요:', end=' ')
                    num = input()
                    num = int(num)

                    with connection.cursor(pms.cursors.DictCursor) as cursor:
                        sql = """SELECT artist_no from participate_song WHERE song_no = %s;"""
                        cursor.execute(sql, song_no)
                        result = cursor.fetchall()
                        connection.commit()

                        sql = """DELETE FROM participate_song WHERE song_no = %s;"""
                        cursor.execute(sql, song_no)
                        connection.commit()

                    for n in range(num):
                        print('\n아티스트 번호를 입력해주세요:', end=' ')
                        input_update = input()
                        try:
                            with connection.cursor() as cursor:
                                sql = """INSERT INTO participate_song VALUES(%s, %s);"""
                                cursor.execute(sql, (song_no, input_update))
                                connection.commit()
                        except pms.err.IntegrityError:
                            print('잘못 입력하셨습니다.')

                            with connection.cursor() as cursor:
                                sql = """DELETE FROM participate_song WHERE song_no = %s;"""
                                cursor.execute(sql, song_no)

                                for row in result:
                                    sql = """INSERT INTO participate_song VALUES(%s, %s);"""
                                    cursor.execute(sql, (song_no, row['artist_no']))

                                connection.commit()
                            return 18

            finally:
                    connection.close()
            return 18

        elif input_no == '2':
            print('삭제하시려면 1을, 취소하려면 아무 키나 입력하세요:', end=' ')
            a = input()

            if a == '1':
                connection = pms.connect(
                    host='localhost',
                    port=3306,
                    user='db',
                    password='db!',
                    db='music',
                    charset='utf8')

                try:
                    with connection.cursor(pms.cursors.DictCursor) as cursor:
                        sql = """DELETE FROM participate_song WHERE song_no = %s;"""
                        cursor.execute(sql, song_no)
                        connection.commit()

                        sql = """DELETE FROM song WHERE song_no = %s;"""
                        cursor.execute(sql, song_no)
                        connection.commit()

                finally:
                    connection.close()
                    print("삭제되었습니다.")

            else:
                print('취소되었습니다.')
            return 17

        else:
            print('잘못 입력하셨습니다. 다시 입력하세요')


def up_del_album():
    """
    19. 앨범 수정/삭제
    """
    connection = pms.connect(
        host='localhost',
        port=3306,
        user='db',
        password='db!',
        db='music',
        charset='utf8')

    global album_no

    try:
        with connection.cursor(pms.cursors.DictCursor) as cursor:
            sql = """SELECT * FROM album_list
                        WHERE album_no = %s;"""
            cursor.execute(sql, album_no)
            result = cursor.fetchone()
            connection.commit()

            if result is None:
                print('잘못 입력하셨습니다.')
                return 17

            print('\n----------------------------------------')
            print('앨범번호: ' + str(result['album_no']))
            print('제목: ' + result['album_title'])
            print('발매일: ' + result['date_of_issue'].strftime('%Y-%m-%d'))
            print('아티스트: ' + result['artist_list'])
            print('----------------------------------------')

    except ValueError:
        print('잘못 입력하셨습니다.')
        return 17

    finally:
        connection.close()

    print('0. 이전화면')
    print('1. 앨범 정보 수정')
    print('2. 앨범 삭제')

    while 1:
        print('입력:', end=' ')
        input_no = input()
        if input_no == '0':
            return 17
        elif input_no == '1':
            print('\n변경하실 정보를 선택하세요.')
            print('0. 수정 취소')
            print('1. 앨범 제목')
            print('2. 발매일')
            print('3. 아티스트')
            print('입력:', end=' ')
            input_no = input()

            connection = pms.connect(
                host='localhost',
                port=3306,
                user='db',
                password='db!',
                db='music',
                charset='utf8')
            try:
                if input_no == '0':
                    return 17
                elif input_no == '1':
                    print('\n변경될 내용을 입력해주세요:', end=' ')
                    input_update = input()
                    with connection.cursor() as cursor:
                        sql = """UPDATE album SET album_title = %s WHERE album_no = %s;"""
                        cursor.execute(sql, (input_update, album_no))
                        connection.commit()

                elif input_no == '2':
                    print('\n변경될 내용을 입력해주세요:', end=' ')
                    input_update = input()
                    with connection.cursor() as cursor:
                        try:
                            sql = """UPDATE album SET date_of_issue = %s WHERE album_no = %s;"""
                            cursor.execute(sql, (input_update, album_no))
                            connection.commit()
                        except pms.err.InternalError:
                            print("발매일은 'YYYY_MM-DD' 형식으로 입력해주세요(ex. 2019-11-27)")

                elif input_no == '3':
                    print('\n입력할 아티스트 수를 입력해주세요:', end=' ')
                    num = input()
                    num = int(num)

                    with connection.cursor(pms.cursors.DictCursor) as cursor:
                        sql = """SELECT artist_no from participate_album WHERE album_no = %s;"""
                        cursor.execute(sql, album_no)
                        result = cursor.fetchall()
                        connection.commit()

                        sql = """DELETE FROM participate_album WHERE album_no = %s;"""
                        cursor.execute(sql, album_no)
                        connection.commit()

                    for n in range(num):
                        print('\n아티스트 번호를 입력해주세요:', end=' ')
                        input_update = input()
                        try:
                            with connection.cursor() as cursor:
                                sql = """INSERT INTO participate_album VALUES(%s, %s);"""
                                cursor.execute(sql, (album_no, input_update))
                                connection.commit()
                        except pms.err.IntegrityError:
                            print('잘못 입력하셨습니다.')
                            with connection.cursor() as cursor:
                                sql = """DELETE FROM participate_album WHERE album_no = %s;"""
                                cursor.execute(sql, album_no)

                                for row in result:
                                    sql = """INSERT INTO participate_album VALUES(%s, %s);"""
                                    cursor.execute(sql, (album_no, row['artist_no']))
                                connection.commit()

                                return 19
            finally:
                connection.close()
            return 19

        elif input_no == '2':
            print('※주의!! 앨범을 삭제하시면 앨범의 수록곡까지 모두 삭제됩니다.')
            print('삭제하시려면 1을, 취소하려면 아무 키나 입력하세요:', end=' ')
            a = input()

            if a == '1':
                connection = pms.connect(
                    host='localhost',
                    port=3306,
                    user='db',
                    password='db!',
                    db='music',
                    charset='utf8')

                try:
                    with connection.cursor() as cursor:
                        sql = """DELETE FROM participate_album WHERE album_no = %s;"""
                        cursor.execute(sql, album_no)
                        connection.commit()

                    with connection.cursor() as cursor:
                        sql = """DELETE FROM album WHERE album_no = %s;"""
                        cursor.execute(sql, album_no)
                        connection.commit()

                finally:
                    connection.close()
                    print("삭제되었습니다.")

            else:
                print('취소되었습니다.')

            return 17

        else:
            print('잘못 입력하셨습니다. 다시 입력하세요')


def insert_song():
    """
    20. 음악 등록
    """
    connection = pms.connect(
        host='localhost',
        port=3306,
        user='db',
        password='db!',
        db='music',
        charset='utf8')

    try:
        print('\n음악 정보를 입력하세요.')
        print('음악 제목:', end=' ')
        song_title = input()

        while 1:
            print('장르:', end=' ')
            genre = input()
            if genre in ('발라드', '댄스', '힙합', '록', '포크', '트로트', 'POP'):
                break
            print("\n잘못 입력하셨습니다(발라드, 댄스, 힙합, 록, 포크, 트로트, POP 중에 입력해주세요)")
            return 17
        print('앨범번호:', end=' ')
        input_album_no = input()

        with connection.cursor() as cursor:
            sql = "SELECT MAX(song_no) FROM song;"
            a = cursor.execute(sql)
            if a == 0:
                no = 0
            else:
                result = cursor.fetchone()
                no = result[0] + 1
            connection.commit()

        with connection.cursor() as cursor:
            sql = "INSERT INTO song VALUES(%s, %s, %s, %s);"
            cursor.execute(sql, (no, song_title, genre, input_album_no))
            connection.commit()

        print('아티스트 수:', end=' ')
        num = input()
        num = int(num)

        for n in range(num):
            print('아티스트번호:', end=' ')
            input_artist_no = input()
            with connection.cursor() as cursor:
                sql = """INSERT INTO participate_song VALUES(%s, %s);"""
                cursor.execute(sql, (no, input_artist_no))
                connection.commit()

        print('\n음악이 등록되었습니다.')

    except pms.err.IntegrityError:
        with connection.cursor() as cursor:
            sql = "DELETE FROM participate_song WHERE song_no = %s"
            cursor.execute(sql, no)
            connection.commit()
            sql = "DELETE FROM song WHERE song_no = %s"
            cursor.execute(sql, no)
            connection.commit()

        print('\n등록되지 않은 번호입니다.')

    finally:
        connection.close()
        return 17


def insert_album():
    """
    21. 앨범 등록
    """
    connection = pms.connect(
        host='localhost',
        port=3306,
        user='db',
        password='db!',
        db='music',
        charset='utf8')

    try:
        print('\n앨범 정보를 입력하세요.')
        print('앨범 제목:', end=' ')
        album_title = input()

        print('발매일(ex. 2019-11-27):', end=' ')
        date_of_issue = input()

        with connection.cursor() as cursor:
            sql = "SELECT MAX(album_no) FROM album;"
            a = cursor.execute(sql)
            if a == 0:
                no = 0
            else:
                result = cursor.fetchone()
                no = result[0] + 1
            connection.commit()

        with connection.cursor() as cursor:
            sql = "INSERT INTO album VALUES(%s, %s, %s);"
            cursor.execute(sql, (no, album_title, date_of_issue))
            connection.commit()

        print('아티스트 수:', end=' ')
        num = input()
        num = int(num)

        for n in range(num):
            print('아티스트번호:', end=' ')
            input_artist_no = input()
            with connection.cursor() as cursor:
                sql = """INSERT INTO participate_album VALUES(%s, %s);"""
                cursor.execute(sql, (no, input_artist_no))
                connection.commit()

        print('\n앨범이 등록되었습니다.')

    except pms.err.IntegrityError:
        with connection.cursor() as cursor:
            sql = "DELETE FROM participate_album WHERE album_no = %s"
            cursor.execute(sql, no)
            connection.commit()
            sql = "DELETE FROM album WHERE album_no = %s"
            cursor.execute(sql, no)
            connection.commit()

        print('\n등록되지 않은 번호입니다.')

    except pms.err.InternalError:
        print("\n발매일은 'YYYY_MM-DD' 형식으로 입력해주세요(ex. 2019-11-27)")

    finally:
        connection.close()
        return 17


def up_del_artist():
    """
    22. 아티스트 수정/삭제
    """
    connection = pms.connect(
        host='localhost',
        port=3306,
        user='db',
        password='db!',
        db='music',
        charset='utf8')

    global artist_no
    is_group = False

    try:
        with connection.cursor(pms.cursors.DictCursor) as cursor:
            sql = """SELECT * FROM artist_list
                    WHERE artist_no = %s;"""
            cursor.execute(sql, artist_no)
            result = cursor.fetchone()
            connection.commit()

            if result is None:
                print('잘못 입력하셨습니다.')
                return 17

            print('\n------------------------------------')
            print('아티스트번호: ' + str(result['artist_no']))
            print('아티스트명: ' + result['artist_name'])
            print('데뷔년도: ' + str(result['debut_year']) + '년')
            print('국적: ' + result['nationality'])
            print('유형: ' + result['type'])
            if result['type'] == '그룹':
                print('멤버: ' + str(result['more_info']))
                is_group = True
            elif result['type'] == '솔로' and result['more_info'] is not None:
                print('소속그룹: ' + result['more_info'])
            print('------------------------------------')

    except ValueError:
        print('잘못 입력하셨습니다.')
        return 17

    finally:
        connection.close()

    print('0. 이전화면')
    print('1. 아티스트 정보 수정')
    print('2. 아티스트 삭제')

    while 1:
        print('입력:', end=' ')
        input_no = input()
        if input_no == '0':
            return 17
        elif input_no == '1':
            print('\n변경하실 정보를 선택하세요.')
            print('0. 수정 취소')
            print('1. 아티스트명')
            print('2. 데뷔년도')
            print('3. 국적')
            if is_group:
                print('4. 멤버')
            print('입력:', end=' ')
            input_no = input()

            connection = pms.connect(
                host='localhost',
                port=3306,
                user='db',
                password='db!',
                db='music',
                charset='utf8')
            try:
                if input_no == '0':
                    return 17
                elif input_no == '1':
                    print('\n변경될 내용을 입력해주세요:', end=' ')
                    input_update = input()
                    with connection.cursor() as cursor:
                        sql = """UPDATE artist SET artist_name = %s WHERE artist_no = %s;"""
                        cursor.execute(sql, (input_update, artist_no))
                        connection.commit()

                elif input_no == '2':
                    print('\n변경될 내용을 입력해주세요:', end=' ')
                    input_update = input()
                    with connection.cursor() as cursor:
                        sql = """UPDATE artist SET debut_year = %s WHERE artist_no = %s;"""
                        cursor.execute(sql, (input_update, artist_no))
                        connection.commit()

                elif input_no == '3':
                    print('\n변경될 내용을 입력해주세요:', end=' ')
                    input_update = input()
                    with connection.cursor() as cursor:
                        sql = """UPDATE artist SET nationality = %s WHERE artist_no = %s;"""
                        cursor.execute(sql, (input_update, artist_no))
                        connection.commit()

                elif input_no == '4' and is_group:
                    print('\n입력할 멤버 수를 입력해주세요:', end=' ')
                    num = input()
                    num = int(num)

                    with connection.cursor(pms.cursors.DictCursor) as cursor:
                        sql = """SELECT member_no from belong_to WHERE group_no = %s;"""
                        cursor.execute(sql, artist_no)
                        result = cursor.fetchall()
                        connection.commit()

                        sql = """DELETE FROM belong_to WHERE group_no = %s;"""
                        cursor.execute(sql, artist_no)
                        connection.commit()

                    for n in range(num):
                        print('\n아티스트 번호를 입력해주세요:', end=' ')
                        input_update = input()
                        try:
                            with connection.cursor() as cursor:
                                sql = """SELECT type FROM artist WHERE artist_no = %s"""
                                cursor.execute(sql, input_update)
                                result2 = cursor.fetchone()

                                if result2[0] == '그룹':
                                    raise pms.err.IntegrityError

                                elif result2[0] == '솔로':
                                    sql = """INSERT INTO belong_to VALUES(%s, %s);"""
                                    cursor.execute(sql, (artist_no, input_update))
                                    connection.commit()

                        except pms.err.IntegrityError:
                            print('등록되지 않은 번호이거나, 그룹 아티스트번호를 입력하였습니다.')

                            with connection.cursor() as cursor:
                                sql = """DELETE FROM belong_to WHERE group_no = %s;"""
                                cursor.execute(sql, artist_no)

                                for row in result:
                                    sql = """INSERT INTO belong_to VALUES(%s, %s);"""
                                    cursor.execute(sql, (artist_no, row['member_no']))

                                connection.commit()
                            return 22

            finally:
                    connection.close()
            return 22

        elif input_no == '2':
            print('삭제하시려면 1을, 취소하려면 아무 키나 입력하세요:', end=' ')
            a = input()

            if a == '1':
                connection = pms.connect(
                    host='localhost',
                    port=3306,
                    user='db',
                    password='db!',
                    db='music',
                    charset='utf8')

                try:
                    with connection.cursor(pms.cursors.DictCursor) as cursor:
                        sql = """DELETE FROM artist WHERE artist_no = %s;"""
                        cursor.execute(sql, artist_no)
                        connection.commit()
                        print("삭제되었습니다.")

                except pms.err.IntegrityError:
                    print('\n참여곡/앨범이 존재하여 삭제할 수 없습니다.')

                finally:
                    connection.close()

            else:
                print('취소되었습니다.')
            return 17

        else:
            print('잘못 입력하셨습니다. 다시 입력하세요')


def insert_artist():
    """
    23. 아티스트 등록
    """
    connection = pms.connect(
        host='localhost',
        port=3306,
        user='db',
        password='db!',
        db='music',
        charset='utf8')

    try:
        print('\n아티스트 정보를 입력하세요.')
        print('아티스트명:', end=' ')
        artist_name = input()

        print('데뷔년도:', end=' ')
        debut_year = input()

        print('국적:', end=' ')
        nationality = input()

        print('유형:', end=' ')
        artist_type = input()
        if artist_type not in ('솔로', '그룹'):
            print("잘못 입력하셨습니다(솔로, 그룹 중에 입력해주세요)")
            return 17

        with connection.cursor() as cursor:
            sql = "SELECT MAX(artist_no) FROM artist;"
            a = cursor.execute(sql)
            if a == 0:
                no = 0
            else:
                result = cursor.fetchone()
                no = result[0] + 1
            connection.commit()

        with connection.cursor() as cursor:
            sql = "INSERT INTO artist VALUES(%s, %s, %s, %s, %s);"
            cursor.execute(sql, (no, artist_name, debut_year, nationality, artist_type))
            connection.commit()

        if artist_type == '그룹':
            print('멤버 수:', end=' ')
            num = input()
            num = int(num)

            for n in range(num):
                print('아티스트번호:', end=' ')
                input_artist_no = input()
                with connection.cursor() as cursor:
                    sql = """SELECT type FROM artist WHERE artist_no = %s"""
                    cursor.execute(sql, input_artist_no)
                    result = cursor.fetchone()

                    if result[0] == '그룹':
                        raise pms.err.IntegrityError

                    elif result[0] == '솔로':
                        sql = """INSERT INTO belong_to VALUES(%s, %s);"""
                        cursor.execute(sql, (no, input_artist_no))
                        connection.commit()

        print('\n아티스트가 등록되었습니다.')

    except pms.err.IntegrityError:
        with connection.cursor() as cursor:
            sql = "DELETE FROM artist WHERE artist_no = %s"
            cursor.execute(sql, no)
            connection.commit()

        print('\n등록되지 않은 번호이거나, 그룹 아티스트번호를 입력하였습니다.')

    finally:
        connection.close()
        return 17


page = 0
user_no = -1
input_title = None
input_artist = None
artist_no = -1
song_no = -1
album_no = -1
admin_no = -1

while 1:
    if page == -1:
        print('\n프로그램을 종료합니다.')
        break
    elif page == 0:  # 첫화면
        page = intro()
    elif page == 1:  # 사용자메뉴
        page = user_menu()
    elif page == 2:  # 로그인
        page = login()
    elif page == 3:  # 사용자메인
        page = user_main()
    elif page == 4:  # 내 플레이리스트 보기
        page = playlist()
    elif page == 5:  # 플레이리스트 삭제
        page = delete_playlist()
    elif page == 6:  # 음악 검색
        page = search_song()
    elif page == 7:  # 회원가입
        page = join()
    elif page == 8:  # 아티스트 검색
        page = search_artist()
    elif page == 9:  # 장르별 음악
        page = search_genre()
    elif page == 10:  # 아티스트 검색
        page = insert_playlist()
    elif page == 11:  # 앨범 정보 보기
        page = album_info()
    elif page == 12:  # 아티스트 정보 보기
        page = artist_info()
    elif page == 13:  # 아티스트 앨범 정보 보기
        page = artist_info_album()
    elif page == 14:  # 아티스트 음악 정보 보기
        page = artist_info_song()
    elif page == 15:  # 관리자메뉴
        page = admin_menu()
    elif page == 16:  # 관리자로그인
        page = admin_login()
    elif page == 17:  # 관리자메인
        page = admin_main()
    elif page == 18:  # 음악 수정/삭제
        page = up_del_song()
    elif page == 19:  # 앨범 수정/삭제
        page = up_del_album()
    elif page == 20:  # 음악 등록
        page = insert_song()
    elif page == 21:  # 앨범 등록
        page = insert_album()
    elif page == 22:  # 아티스트 수정/삭제
        page = up_del_artist()
    elif page == 23:  # 아티스트 등록
        page = insert_artist()

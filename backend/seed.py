from database import get_conn, init_db


def seed():
    conn = get_conn()
    c = conn.cursor()

    # Check if already seeded — prevents duplicate data
    # if you accidentally run this file twice
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] > 0:
        print("⚠️  Database already seeded. Skipping.")
        conn.close()
        return

    print("🌱 Seeding database...")

    # ── STEP 1: AUTHORS ───────────────────────────────────────────────────────
    # We insert authors first because books need author_id
    # Each tuple matches the columns:
    # (name, birth_year, death_year, nationality, bio)
    authors = [
        (
            "Jane Austen", 1775, 1817, "British",
            "Jane Austen was an English novelist known primarily for her "
            "six major novels which interpret, critique and comment upon "
            "the British landed gentry at the end of the 18th century."
        ),
        (
            "Arthur Conan Doyle", 1859, 1930, "British",
            "Sir Arthur Conan Doyle was a British author best known for "
            "his detective fiction featuring Sherlock Holmes."
        ),
        (
            "Charles Dickens", 1812, 1870, "British",
            "Charles Dickens was an English novelist and social critic "
            "who created some of the world's best-known fictional characters."
        ),
        (
            "Mary Shelley", 1797, 1851, "British",
            "Mary Shelley was an English novelist who wrote the Gothic "
            "novel Frankenstein, or The Modern Prometheus."
        ),
        (
            "Bram Stoker", 1847, 1912, "Irish",
            "Bram Stoker was an Irish author best known today for his "
            "1897 Gothic horror novel Dracula."
        ),
        (
            "Lewis Carroll", 1832, 1898, "British",
            "Lewis Carroll was an English author, poet and mathematician "
            "best known for Alice's Adventures in Wonderland."
        ),
        (
            "Herman Melville", 1819, 1891, "American",
            "Herman Melville was an American novelist best known for "
            "Moby-Dick and his early novels based on his experiences in "
            "the South Pacific."
        ),
        (
            "Fyodor Dostoevsky", 1821, 1881, "Russian",
            "Fyodor Dostoevsky was a Russian novelist whose works explore "
            "human psychology in the troubled political, social and "
            "spiritual atmosphere of 19th-century Russia."
        ),
        (
            "Mark Twain", 1835, 1910, "American",
            "Mark Twain was an American writer, humorist and lecturer "
            "best known for The Adventures of Tom Sawyer and "
            "Adventures of Huckleberry Finn."
        ),
        (
            "Franz Kafka", 1883, 1924, "Czech",
            "Franz Kafka was a German-speaking Bohemian novelist whose "
            "works, such as The Metamorphosis and The Trial, are marked "
            "by themes of alienation and existential anxiety."
        ),
    ]

    c.executemany("""
        INSERT INTO authors (name, birth_year, death_year, nationality, bio)
        VALUES (?, ?, ?, ?, ?)
    """, authors)

    print(f"  ✅ {len(authors)} authors inserted")

    # ── STEP 2: BOOKS ─────────────────────────────────────────────────────────
    # We fetch author IDs by name so we don't hardcode them.
    # This is safer — IDs are auto-generated and may vary.
    def author_id(name):
        row = c.execute(
            "SELECT id FROM authors WHERE name=?", (name,)
        ).fetchone()
        return row["id"] if row else None

    # Each tuple:
    # (gutenberg_id, title, author_id, genre, cover_url,
    #  total_pages, description, publish_year)
    books = [
        (
            1342, "Pride and Prejudice", author_id("Jane Austen"),
            "Romance",
            "https://covers.openlibrary.org/b/id/8739161-M.jpg",
            432,
            "The story follows the main character Elizabeth Bennet as she "
            "deals with issues of manners, upbringing, morality, education "
            "and marriage in the society of the British landed gentry.",
            1813
        ),
        (
            1661, "The Adventures of Sherlock Holmes",
            author_id("Arthur Conan Doyle"),
            "Mystery",
            "https://covers.openlibrary.org/b/id/8406786-M.jpg",
            307,
            "A collection of twelve stories featuring the brilliant "
            "detective Sherlock Holmes and his partner Dr. Watson.",
            1892
        ),
        (
            2852, "The Hound of the Baskervilles",
            author_id("Arthur Conan Doyle"),
            "Mystery",
            "https://covers.openlibrary.org/b/id/8739601-M.jpg",
            256,
            "Sherlock Holmes investigates the legend of a supernatural "
            "hound threatening the Baskerville family.",
            1902
        ),
        (
            98, "A Tale of Two Cities", author_id("Charles Dickens"),
            "Historical",
            "https://covers.openlibrary.org/b/id/9327027-M.jpg",
            489,
            "A historical novel set in London and Paris before and during "
            "the French Revolution.",
            1859
        ),
        (
            1400, "Great Expectations", author_id("Charles Dickens"),
            "Literary Fiction",
            "https://covers.openlibrary.org/b/id/9327027-M.jpg",
            544,
            "The story of orphan Pip and his journey from childhood "
            "poverty to adult wealth, exploring themes of ambition and "
            "self-improvement.",
            1861
        ),
        (
            84, "Frankenstein", author_id("Mary Shelley"),
            "Horror",
            "https://covers.openlibrary.org/b/id/8231856-M.jpg",
            280,
            "A scientist creates a sapient creature in an unorthodox "
            "scientific experiment. Often considered the first science "
            "fiction novel.",
            1818
        ),
        (
            345, "Dracula", author_id("Bram Stoker"),
            "Horror",
            "https://covers.openlibrary.org/b/id/8739601-M.jpg",
            418,
            "The story of Count Dracula's attempt to move from "
            "Transylvania to England, told through journal entries "
            "and letters.",
            1897
        ),
        (
            11, "Alice's Adventures in Wonderland",
            author_id("Lewis Carroll"),
            "Fantasy",
            "https://covers.openlibrary.org/b/id/8739415-M.jpg",
            192,
            "A young girl named Alice falls through a rabbit hole into "
            "a fantasy world populated by peculiar creatures.",
            1865
        ),
        (
            2701, "Moby Dick", author_id("Herman Melville"),
            "Adventure",
            "https://covers.openlibrary.org/b/id/8739532-M.jpg",
            635,
            "The obsessive quest of Ahab, captain of the whaling ship "
            "Pequod, for revenge on Moby Dick, a giant white sperm whale.",
            1851
        ),
        (
            2554, "Crime and Punishment",
            author_id("Fyodor Dostoevsky"),
            "Psychological",
            "https://covers.openlibrary.org/b/id/8739161-M.jpg",
            671,
            "A student in Saint Petersburg commits a murder and "
            "subsequently struggles with guilt and paranoia.",
            1866
        ),
        (
            74, "The Adventures of Tom Sawyer",
            author_id("Mark Twain"),
            "Adventure",
            "https://covers.openlibrary.org/b/id/8406786-M.jpg",
            274,
            "The story of a young boy growing up along the Mississippi "
            "River who gets into all kinds of mischief.",
            1876
        ),
        (
            1080, "The Metamorphosis", author_id("Franz Kafka"),
            "Literary Fiction",
            "https://covers.openlibrary.org/b/id/8739492-M.jpg",
            128,
            "A salesman wakes one morning to find himself transformed "
            "into a giant insect. A profound exploration of alienation.",
            1915
        ),
    ]

    c.executemany("""
        INSERT INTO books
            (gutenberg_id, title, author_id, genre, cover_url,
             total_pages, description, publish_year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, books)

    print(f"  ✅ {len(books)} books inserted")

    # ── STEP 3: USERS ─────────────────────────────────────────────────────────
    # Demo users — each has a different reading taste
    # This variety is important for the recommendation engine
    # to find meaningful patterns
    # (username, display_name, email, avatar_emoji, bio)
    users = [
        (
            "priya_reads", "Priya Sharma",
            "priya@example.com", "🌸",
            "Loves classics and romance novels"
        ),
        (
            "rahul_books", "Rahul Verma",
            "rahul@example.com", "🎯",
            "Mystery and thriller addict"
        ),
        (
            "ananya_lit", "Ananya Iyer",
            "ananya@example.com", "✨",
            "Horror and dark fiction fan"
        ),
        (
            "karthik_r", "Karthik Rao",
            "karthik@example.com", "🚀",
            "Adventure and psychological fiction"
        ),
        (
            "meera_pages", "Meera Nair",
            "meera@example.com", "🌿",
            "Historical fiction and literary classics"
        ),
    ]

    c.executemany("""
        INSERT INTO users
            (username, display_name, email, avatar_emoji, bio)
        VALUES (?, ?, ?, ?, ?)
    """, users)

    print(f"  ✅ {len(users)} users inserted")

    # ── STEP 4: SHELF (USER_BOOKS) ────────────────────────────────────────────
    # This data powers the recommendation engine.
    # Each user has different reading history and ratings.
    # The collaborative filter uses this to find similar users.
    #
    # Format: (user_id, book_id, status, current_page,
    #          rating, date_started, date_finished)
    #
    # user IDs: priya=1, rahul=2, ananya=3, karthik=4, meera=5
    # book IDs: pride=1, sherlock=2, hound=3, two_cities=4,
    #           great_exp=5, frankenstein=6, dracula=7,
    #           alice=8, moby=9, crime=10, tom=11, metamorphosis=12

    user_books = [
        # Priya — loves Romance and Historical
        (1, 1, "finished", 432, 5, "2026-01-05", "2026-01-20"),
        (1, 4, "finished", 489, 4, "2026-01-22", "2026-02-10"),
        (1, 5, "finished", 544, 5, "2026-02-12", "2026-03-01"),
        (1, 8, "finished", 192, 4, "2026-03-03", "2026-03-07"),
        (1, 2, "reading",  120, 0, "2026-03-08", None),

        # Rahul — loves Mystery
        (2, 2, "finished", 307, 5, "2026-01-10", "2026-01-22"),
        (2, 3, "finished", 256, 5, "2026-01-24", "2026-02-05"),
        (2, 10, "finished", 671, 4, "2026-02-07", "2026-03-01"),
        (2, 7, "reading",  200, 0, "2026-03-05", None),

        # Ananya — loves Horror
        (3, 6, "finished", 280, 5, "2026-01-03", "2026-01-15"),
        (3, 7, "finished", 418, 5, "2026-01-17", "2026-01-30"),
        (3, 2, "finished", 307, 4, "2026-02-01", "2026-02-14"),
        (3, 3, "finished", 256, 4, "2026-02-16", "2026-02-25"),
        (3, 12, "reading", 80,  0, "2026-03-01", None),

        # Karthik — loves Adventure and Psychological
        (4, 9,  "finished", 635, 4, "2026-01-08", "2026-02-01"),
        (4, 11, "finished", 274, 4, "2026-02-03", "2026-02-15"),
        (4, 10, "finished", 671, 5, "2026-02-17", "2026-03-05"),
        (4, 12, "finished", 128, 5, "2026-03-06", "2026-03-09"),

        # Meera — loves Historical and Literary Fiction
        (5, 1, "finished", 432, 4, "2026-01-06", "2026-01-25"),
        (5, 4, "finished", 489, 5, "2026-01-27", "2026-02-12"),
        (5, 5, "finished", 544, 5, "2026-02-14", "2026-03-02"),
        (5, 9, "reading",  300, 0, "2026-03-04", None),
    ]

    c.executemany("""
        INSERT INTO user_books
            (user_id, book_id, status, current_page,
             rating, date_started, date_finished)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, user_books)

    print(f"  ✅ {len(user_books)} shelf entries inserted")

    # ── STEP 5: REVIEWS ───────────────────────────────────────────────────────
    # Written reviews with varied opinions.
    # These feed the reviews page and also signal user taste
    # for the recommendation engine.
    # (user_id, book_id, rating, title, body, is_spoiler)
    reviews = [
        (
            1, 1, 5,
            "A timeless masterpiece",
            "Pride and Prejudice is one of those rare books that gets "
            "better every time you read it. Austen's wit and her "
            "portrayal of Elizabeth Bennet is just extraordinary. "
            "The romance feels real and earned.",
            0
        ),
        (
            2, 2, 5,
            "Holmes at his absolute best",
            "The Adventures of Sherlock Holmes is the perfect introduction "
            "to the world's greatest detective. Every story is a gem. "
            "The logic, the atmosphere, the characters — all perfect.",
            0
        ),
        (
            3, 6, 5,
            "The original and still the best",
            "Frankenstein is not just a horror novel — it is a profound "
            "meditation on creation, responsibility and what it means to "
            "be human. Mary Shelley was centuries ahead of her time.",
            0
        ),
        (
            3, 7, 5,
            "Genuinely terrifying even today",
            "Dracula still manages to be deeply unsettling despite being "
            "over 100 years old. The epistolary format makes it feel "
            "incredibly real and immediate.",
            0
        ),
        (
            4, 10, 5,
            "Changed the way I think",
            "Crime and Punishment is brutal, brilliant and unforgettable. "
            "Dostoevsky gets inside a criminal's mind with terrifying "
            "accuracy. One of the greatest novels ever written.",
            0
        ),
        (
            5, 4, 5,
            "Dickens at the height of his powers",
            "A Tale of Two Cities is sweeping, emotional and beautifully "
            "written. The opening line is one of the most famous in all "
            "of literature for good reason.",
            0
        ),
        (
            1, 8, 4,
            "Delightfully strange",
            "Alice in Wonderland is wonderfully weird. Carroll's wordplay "
            "and imagination are on full display. A quick and charming "
            "read that works on multiple levels.",
            0
        ),
        (
            4, 12, 5,
            "Short but devastating",
            "The Metamorphosis packs more meaning into 128 pages than "
            "most novels manage in 600. Kafka's vision of alienation "
            "feels more relevant now than ever.",
            0
        ),
    ]

    c.executemany("""
        INSERT INTO reviews
            (user_id, book_id, rating, title, body, is_spoiler)
        VALUES (?, ?, ?, ?, ?, ?)
    """, reviews)

    print(f"  ✅ {len(reviews)} reviews inserted")

    # ── STEP 6: HIGHLIGHTS ────────────────────────────────────────────────────
    # Famous quotes from the books.
    # These appear on the highlights page and also tell the
    # recommendation engine which books users engaged with deeply.
    # (user_id, book_id, quote, page_number, note)
    highlights = [
        (
            1, 1,
            "It is a truth universally acknowledged, that a single man "
            "in possession of a good fortune, must be in want of a wife.",
            1,
            "The most famous opening line in English literature!"
        ),
        (
            2, 2,
            "When you have eliminated the impossible, whatever remains, "
            "however improbable, must be the truth.",
            87,
            "The most iconic Holmes quote — pure logic."
        ),
        (
            2, 2,
            "The game is afoot.",
            45,
            "Short but so dramatic!"
        ),
        (
            3, 6,
            "Beware; for I am fearless, and therefore powerful.",
            156,
            "The creature's most chilling line."
        ),
        (
            3, 7,
            "I am longing to be with you, and by the sea, where we can "
            "talk together freely and build our castles in the air.",
            203,
            "Beautiful and eerie at the same time."
        ),
        (
            4, 10,
            "Pain and suffering are always inevitable for a large "
            "intelligence and a deep heart.",
            312,
            "Dostoevsky understood the human condition completely."
        ),
        (
            5, 4,
            "It was the best of times, it was the worst of times.",
            1,
            "The greatest opening line ever written."
        ),
        (
            1, 5,
            "I have been bent and broken, but I hope into a better shape.",
            287,
            "Pip's growth in one sentence."
        ),
    ]

    c.executemany("""
        INSERT INTO highlights
            (user_id, book_id, quote, page_number, note)
        VALUES (?, ?, ?, ?, ?)
    """, highlights)

    print(f"  ✅ {len(highlights)} highlights inserted")

    conn.commit()
    conn.close()
    print("\n🎉 Database seeded successfully! Ready to run the app.")


if __name__ == "__main__":
    init_db()   # make sure tables exist first
    seed()      # then fill them with data
from app.database import db
from app.models import LESSONS_COLLECTION, USER_LESSONS_COLLECTION
from google.cloud.firestore import SERVER_TIMESTAMP

# Pre-defined lessons: 30 topics with title, content, quiz, correct answer
def get_predefined_lessons():
    lessons = [
        {
            "id": "lesson_1",
            "title": "What is a stock?",
            "content": "A stock represents a share in the ownership of a company. When you buy a stock, you become a partial owner. Companies issue stocks to raise capital for growth.",
            "quiz_question": "What does a stock represent? (A) A loan to the company (B) A share of ownership (C) A guaranteed profit",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_2",
            "title": "Why long-term investing beats trading",
            "content": "Long-term investing benefits from compound growth and avoids the stress of timing the market. Traders often lose due to fees and emotional decisions.",
            "quiz_question": "Which is generally better for most people? (A) Day trading (B) Long-term investing (C) Short selling",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_3",
            "title": "Difference between betting and investing",
            "content": "Investing is based on research and fundamentals, aiming for long-term growth. Betting relies on luck and short-term outcomes. Investors manage risk; bettors gamble.",
            "quiz_question": "Investing is like: (A) Gambling in a casino (B) Buying a business with research (C) Lottery ticket",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_4",
            "title": "The power of compound interest",
            "content": "Compound interest means earning returns on your returns. Over decades, small amounts grow exponentially. Start early to maximize wealth.",
            "quiz_question": "Compound interest works best when: (A) You start late (B) You reinvest earnings (C) You withdraw profits yearly",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_5",
            "title": "Understanding P/E ratio",
            "content": "Price-to-Earnings ratio compares stock price to company earnings per share. A high P/E may mean overvalued; low P/E could be undervalued or troubled.",
            "quiz_question": "A low P/E ratio might indicate: (A) Overvalued stock (B) Undervalued or troubled stock (C) Guaranteed profit",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_6",
            "title": "What are blue chip stocks?",
            "content": "Blue chips are shares of large, reputable, financially sound companies with stable earnings. Examples in Philippines: SM, Ayala, BDO.",
            "quiz_question": "Blue chip stocks are known for: (A) High risk (B) Stability and reliability (C) Penny stock volatility",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_7",
            "title": "Diversification explained",
            "content": "Diversification means spreading money across different assets (stocks, sectors, countries) to reduce risk. Don't put all eggs in one basket.",
            "quiz_question": "The main goal of diversification is: (A) Maximize short-term returns (B) Reduce overall risk (C) Avoid taxes",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_8",
            "title": "How dividends work",
            "content": "Dividends are portions of a company's profit paid to shareholders. They provide regular income. Not all companies pay dividends; growth stocks reinvest profits.",
            "quiz_question": "Dividends are: (A) Guaranteed interest (B) Profit sharing with shareholders (C) Trading fees",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_9",
            "title": "Market volatility – don't panic",
            "content": "Volatility is normal. Prices go up and down. Panic selling locks in losses. Stay calm and focus on long-term goals.",
            "quiz_question": "During market dips, a wise investor should: (A) Panic sell (B) Stay calm and review strategy (C) Borrow money to short",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_10",
            "title": "Investor mindset: patience",
            "content": "Patience allows investments to grow. The market rewards those who wait. Avoid chasing quick profits.",
            "quiz_question": "Which trait is most important for long-term investing? (A) Patience (B) Impulsiveness (C) Overtrading",
            "quiz_correct_answer": "A"
        },
        {
            "id": "lesson_11",
            "title": "Investor mindset: discipline",
            "content": "Discipline means sticking to your investment plan even when emotions run high. It prevents buying high and selling low.",
            "quiz_question": "Discipline helps you: (A) Follow a plan (B) Trade randomly (C) Ignore research",
            "quiz_correct_answer": "A"
        },
        {
            "id": "lesson_12",
            "title": "Investor mindset: no greed",
            "content": "Greed leads to excessive risk and chasing bubbles. Greedy investors often lose. Take reasonable profits and stay grounded.",
            "quiz_question": "Greed in investing often results in: (A) Sustainable wealth (B) Losses and mistakes (C) Guaranteed returns",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_13",
            "title": "Fundamental vs technical analysis",
            "content": "Fundamental analysis studies company financials and industry. Technical analysis studies price charts and patterns. Both can be useful.",
            "quiz_question": "Which analysis looks at company earnings? (A) Technical (B) Fundamental (C) Astrological",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_14",
            "title": "What is a bear market?",
            "content": "A bear market is when prices drop 20% or more from recent highs, often accompanied by pessimism. It can be a buying opportunity for long-term investors.",
            "quiz_question": "Bear markets are characterized by: (A) Rising prices (B) Falling prices (C) No movement",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_15",
            "title": "What is a bull market?",
            "content": "A bull market is a prolonged period of rising stock prices, usually with optimism and economic growth. It's when most investors profit.",
            "quiz_question": "Bull markets are characterized by: (A) Falling prices (B) Rising prices (C) High volatility only",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_16",
            "title": "How to read a candlestick chart",
            "content": "Candlesticks show open, high, low, close (OHLC). Green/white means price rose; red/black means price fell. Patterns help predict movement.",
            "quiz_question": "A green candlestick indicates: (A) Price closed higher than open (B) Price closed lower than open (C) No change",
            "quiz_correct_answer": "A"
        },
        {
            "id": "lesson_17",
            "title": "Importance of volume",
            "content": "Volume is the number of shares traded. High volume confirms price trends; low volume may signal weak moves. Use volume to validate breakouts.",
            "quiz_question": "High volume during a price rally suggests: (A) Weak trend (B) Strong conviction (C) Reversal coming",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_18",
            "title": "What is market capitalization?",
            "content": "Market cap = share price × total shares. Large-cap (over $10B) are stable; mid-cap ($2B-$10B); small-cap (under $2B) more volatile.",
            "quiz_question": "Large-cap companies generally have: (A) Higher risk (B) More stability (C) Zero volatility",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_19",
            "title": "What is EPS (Earnings Per Share)?",
            "content": "EPS = net profit divided by number of shares. Higher EPS means more profit per share. Compare EPS over time to gauge growth.",
            "quiz_question": "Increasing EPS is generally: (A) Bad for shareholders (B) Good for shareholders (C) Irrelevant",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_20",
            "title": "What is ROE (Return on Equity)?",
            "content": "ROE measures how efficiently a company uses shareholders' equity to generate profit. ROE above 15% is considered good.",
            "quiz_question": "A high ROE indicates: (A) Inefficient management (B) Effective use of equity (C) High debt",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_21",
            "title": "How to spot a dying company (avoid)",
            "content": "Warning signs: falling revenues, high debt, negative earnings, management scandals, obsolete products. Avoid such stocks.",
            "quiz_question": "Which is a red flag for a dying company? (A) Growing profits (B) High debt and losses (C) Increasing dividends",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_22",
            "title": "How to spot a growing company (good)",
            "content": "Look for increasing revenues, expanding margins, low debt, competitive advantage, and good management. These are potential winners.",
            "quiz_question": "A growing company typically shows: (A) Declining sales (B) Rising profits and market share (C) Frequent lawsuits",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_23",
            "title": "The risk of penny stocks",
            "content": "Penny stocks are cheap, highly speculative, easily manipulated, and often illiquid. Most retail investors lose money on them.",
            "quiz_question": "Penny stocks are generally: (A) Safe investments (B) Highly risky and speculative (C) Blue chip equivalents",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_24",
            "title": "Why index funds are safe",
            "content": "Index funds track a market index (e.g., PSEi). They are diversified, low-cost, and outperform most active managers over long term.",
            "quiz_question": "Index funds are considered: (A) High risk (B) Low-cost and diversified (C) Active trading tools",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_25",
            "title": "How inflation affects stocks",
            "content": "Inflation erodes purchasing power. Moderate inflation is normal; high inflation can hurt stocks by raising costs and interest rates.",
            "quiz_question": "High inflation typically: (A) Helps all stocks (B) Can hurt stocks via rate hikes (C) No effect",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_26",
            "title": "What are interest rates doing?",
            "content": "Central banks raise rates to fight inflation, which can lower stock prices. Lower rates stimulate growth and often boost stocks.",
            "quiz_question": "Rising interest rates generally: (A) Boost stock prices (B) Pressure stock prices (C) Have no impact",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_27",
            "title": "Rebalancing your portfolio",
            "content": "Rebalancing means selling winners and buying losers to maintain target asset allocation. It locks profits and manages risk.",
            "quiz_question": "Rebalancing helps you: (A) Increase risk (B) Maintain desired risk level (C) Time the market",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_28",
            "title": "Dollar cost averaging",
            "content": "Investing fixed amount regularly regardless of price. It reduces impact of volatility and removes emotion from timing.",
            "quiz_question": "Dollar cost averaging: (A) Invests all at once (B) Invests same amount periodically (C) Tries to time lows",
            "quiz_correct_answer": "B"
        },
        {
            "id": "lesson_29",
            "title": "Tax on stock gains (Philippines)",
            "content": "Stock transactions on PSE are subject to 0.1% transaction tax on sale. Dividends have 10% withholding tax for individuals.",
            "quiz_question": "In the Philippines, stock sales incur: (A) 0.1% transaction tax (B) 20% capital gains (C) No tax",
            "quiz_correct_answer": "A"
        },
        {
            "id": "lesson_30",
            "title": "When to sell a stock",
            "content": "Sell if the company's fundamentals deteriorate, you need cash, or it becomes overvalued. Don't sell based on short-term fear.",
            "quiz_question": "A good reason to sell is: (A) Stock dropped 5% (B) Company's business is permanently broken (C) Friend told you to sell",
            "quiz_correct_answer": "B"
        }
    ]
    return lessons

def seed_lessons_if_empty():
    """Check if lessons collection is empty; if yes, insert predefined lessons."""
    lessons_ref = db.collection(LESSONS_COLLECTION)
    existing = lessons_ref.limit(1).get()
    if len(list(existing)) > 0:
        return  # Already seeded

    lessons = get_predefined_lessons()
    for lesson in lessons:
        doc_ref = lessons_ref.document(lesson["id"])
        doc_ref.set(lesson)
    print(f"Seeded {len(lessons)} lessons to Firestore.")

def get_all_lessons():
    """Return all lessons sorted by order_index (using id numeric suffix)."""
    lessons_ref = db.collection(LESSONS_COLLECTION)
    docs = lessons_ref.stream()
    lessons = []
    for doc in docs:
        lesson = doc.to_dict()
        lesson["id"] = doc.id
        # Extract numeric order from id "lesson_X"
        if "id" in lesson:
            try:
                lesson["order_index"] = int(lesson["id"].split("_")[1])
            except:
                lesson["order_index"] = 999
        else:
            lesson["order_index"] = 999
        lessons.append(lesson)
    lessons.sort(key=lambda x: x["order_index"])
    # Remove internal order_index before returning
    for l in lessons:
        if "order_index" in l:
            del l["order_index"]
    return lessons

def get_lesson_by_id(lesson_id):
    """Return a single lesson dict or None."""
    doc_ref = db.collection(LESSONS_COLLECTION).document(lesson_id)
    doc = doc_ref.get()
    if not doc.exists:
        return None
    lesson = doc.to_dict()
    lesson["id"] = doc.id
    return lesson

def mark_lesson_complete(user_id: str, lesson_id: str, user_answer: str, correct_answer: str) -> bool:
    """Check if answer matches, then store completion. Returns True if correct and saved."""
    if user_answer.strip() != correct_answer.strip():
        return False
    # Store completion
    user_lesson_ref = db.collection(USER_LESSONS_COLLECTION).document(f"{user_id}_{lesson_id}")
    user_lesson_ref.set({
        "user_id": user_id,
        "lesson_id": lesson_id,
        "completed_at": SERVER_TIMESTAMP
    })
    return True

def get_user_completed_lessons(user_id: str):
    """Return list of lesson_ids that user has completed."""
    user_lessons_ref = db.collection(USER_LESSONS_COLLECTION).where("user_id", "==", user_id)
    docs = user_lessons_ref.stream()
    completed_ids = [doc.to_dict().get("lesson_id") for doc in docs if doc.to_dict().get("lesson_id")]
    return completed_ids
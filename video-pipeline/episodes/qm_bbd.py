# The Quiet Money, episode 1: "Buy, Borrow, Die" (long-form, ~9-10 min).
# Facts: ProPublica "The Secret IRS Files" (June 2021); IRS/US tax code (37% top rate, 20% + 3.8% capital gains,
# step-up in basis, 40% estate tax, ~$15M exemption per person from 2026); Edward McCaffery (USC) coined the term.
SCENES_MODULE = "finance_scenes"
AMBIENT = "finance"
CAPTIONS = False
XFADE = 0.3
FADE = 0.001
GAP, TAIL = 0.3, 0.5
EL_VOICE = "cjVigY5qzO86Huf0OWal"   # Eric: smooth, trustworthy American narrator
EL_SETTINGS = dict(stability=0.45, similarity_boost=0.8, style=0.15, speed=0.98)
FINAL = "x264"
PRON = {"401(k)": "four-oh-one-k", "IRS": "I R S", "ProPublica": "Pro Publica", "McCaffery": "Mc-Caffery",
        "$81,840": "eighty-one thousand, eight hundred and forty dollars"}

LONG = [
    # ---------- cold open ----------
    dict(scene="zero_tax", args=dict(year="2018"), text=[
        "In 2018, one of the richest people on Earth paid zero dollars in federal income tax.",
        "Not a typo. Not a crime. Zero.",
    ]),
    dict(scene="vs_teacher", text=[
        "That same year, a teacher earning sixty thousand dollars paid roughly eleven thousand in federal income and payroll taxes.",
        "Taken out of every paycheck, before she ever saw the money.",
    ]),
    dict(scene="rate_bars", text=[
        "When journalists at ProPublica got hold of leaked IRS data, they found that the twenty-five richest Americans paid a true tax rate of just three point four percent.",
        "The typical American household? Around fourteen percent.",
    ]),
    dict(scene="zero_list", text=[
        "And it's not one person, or one strange year.",
        "According to the same leaked records, Elon Musk paid zero in 2018.",
        "Jeff Bezos paid zero in 2007, and again in 2011, when he even claimed a four thousand dollar tax credit for his children.",
        "Michael Bloomberg, Carl Icahn and George Soros all had years where they paid nothing too.",
    ]),
    dict(scene="question", text=[
        "So how do people worth billions legally pay less than the people who teach their kids?",
        "The answer is a three-step playbook that tax lawyers have used for decades.",
    ]),
    dict(scene="title", text=["It's called: Buy. Borrow. Die."]),
    # ---------- chapter 1 ----------
    dict(scene="two_money", args=dict(chap="1 · Two kinds of money"), text=[
        "To understand it, you need to know one thing about the tax system.",
        "It doesn't tax how rich you are. It taxes income.",
        "And there are two very different kinds of money.",
    ]),
    dict(scene="paycheck", text=[
        "The first is income: your salary, your wages, your bonus.",
        "That money is taxed automatically. Federal tax, state tax, social security, medicare.",
        "The government takes its share before the money even reaches your account.",
    ]),
    dict(scene="stock_grow", text=[
        "The second kind is wealth: things you own that grow in value. Stocks, companies, real estate.",
        "If your shares go from one million to one billion dollars, how much tax do you owe on that growth?",
        "Nothing. Not a single dollar.",
        "Until you sell, it's an unrealized gain. And unrealized gains are not taxed.",
    ]),
    dict(scene="salary_vs_stock", text=[
        "This is why the richest people often have surprisingly small salaries.",
        "For years, Jeff Bezos's salary at Amazon was about $81,840.",
        "His real fortune was his stock, worth well over a hundred billion dollars, growing quietly, untaxed.",
    ]),
    # ---------- step 1 ----------
    dict(scene="step_buy", args=dict(chap="2 · Step one: Buy"), text=[
        "Which brings us to step one: buy.",
        "Buy assets that grow. Shares of your own company, the stock market, buildings, land.",
    ]),
    dict(scene="never_sell", text=[
        "Then, the most important rule of all: never sell.",
        "Selling is what turns wealth into taxable income.",
        "As long as you hold, the IRS has nothing to tax.",
    ]),
    dict(scene="need_cash", text=[
        "But there's a problem.",
        "Billionaires have bills too. Houses, jets, staff, yachts.",
        "If they never sell, where does the cash come from?",
    ]),
    dict(scene="sell_tax", text=[
        "Selling stock would trigger capital gains tax, up to twenty percent, plus a three point eight percent investment tax on top.",
        "On a billion-dollar sale, that's more than two hundred million dollars gone.",
        "So instead, they do something that most people never think of.",
    ]),
    # ---------- step 2 ----------
    dict(scene="borrow_bank", args=dict(chap="3 · Step two: Borrow"), text=[
        "Step two: borrow.",
        "They go to a bank and pledge their shares as collateral, the same way your house backs a mortgage.",
        "The bank hands them cash. Millions, sometimes hundreds of millions.",
    ]),
    dict(scene="loan_not_income", text=[
        "And here's the trick. A loan is not income.",
        "You have to pay it back, so the IRS doesn't tax it.",
        "Borrowed money arrives tax free.",
    ]),
    dict(scene="loan_math", text=[
        "For the very rich, the math is beautiful.",
        "Say your portfolio is worth one hundred million dollars and grows seven percent a year. That's seven million.",
        "You borrow three million to live on, at four percent interest. That costs you one hundred and twenty thousand dollars a year.",
        "Your wealth grows much faster than your debt. And you never paid income tax on any of it.",
    ]),
    dict(scene="filings", text=[
        "This isn't a theory. It's in public company filings.",
        "Elon Musk has pledged large amounts of Tesla stock to secure personal loans.",
        "Oracle's founder Larry Ellison has pledged Oracle shares to back his credit lines.",
    ]),
    dict(scene="rollover", text=[
        "And when a loan comes due? Many simply take out a new loan to pay off the old one.",
        "Borrow, roll it over, borrow again. For decades.",
        "Which leads to the final step.",
    ]),
    dict(scene="scale", text=[
        "Can regular people do this? Partly. Many brokers offer loans against your investments, often called a securities-based line of credit.",
        "The difference is scale. Borrowing three percent of a fifty thousand dollar portfolio gets you fifteen hundred dollars.",
        "Three percent of a hundred billion dollar fortune is three billion. Enough to live like royalty, forever.",
    ]),
    # ---------- step 3 ----------
    dict(scene="step_die", args=dict(chap="4 · Step three: Die"), text=[
        "Step three: die.",
        "It sounds dark, but this is where the biggest tax break of all is hiding.",
    ]),
    dict(scene="step_up", text=[
        "Imagine you bought shares for one million dollars, and when you die, they're worth one billion.",
        "Normally, selling them would mean tax on nine hundred and ninety-nine million dollars of profit.",
        "But when your heirs inherit those shares, the law resets their cost to today's value. One billion.",
        "It's called the step-up in basis. If they sell the next day, the taxable gain is close to zero.",
        "Decades of growth. Never taxed as income. Ever.",
    ]),
    dict(scene="estate", text=[
        "There is an estate tax: forty percent on fortunes above roughly fifteen million dollars per person.",
        "But the wealthy have armies of lawyers, and trusts designed to shrink that bill, sometimes dramatically.",
    ]),
    dict(scene="heirs_repay", text=[
        "Then the heirs sell a small slice of the stepped-up shares, repay all those loans, and keep the rest.",
        "The debt is gone. The tax on the growth never arrived.",
    ]),
    dict(scene="cycle", text=[
        "Buy assets that grow. Borrow against them instead of selling. Hold them until death, and pass them on with a fresh, stepped-up value.",
        "That's how a fortune can grow for generations, while the income tax on it stays close to zero.",
        "No secret loophole. Just patience, and very good lawyers.",
    ]),
    dict(scene="story", args=dict(chap="Putting it together"), text=[
        "Let's run the whole playbook on an imaginary founder. Call him Alex.",
        "At thirty, Alex starts a company and keeps half of it. By fifty, his stake is worth five billion dollars. His salary? One dollar.",
        "Every year, he borrows fifty million against his shares to live on. Over thirty years, that's one and a half billion dollars of spending, and zero income tax.",
        "At eighty, Alex dies. His shares, now worth twenty billion, pass to his kids with a stepped-up basis.",
        "They sell just enough to repay the loans and the interest. Capital gains tax on that sale: practically nothing.",
        "A lifetime of growth, worth twenty billion dollars, and almost no income tax was ever paid on it.",
    ]),
    # ---------- chapter 5 ----------
    dict(scene="legal", args=dict(chap="5 · Is this legal?"), text=[
        "Is this legal? Completely.",
        "The name Buy, Borrow, Die was popularized by USC law professor Edward McCaffery, who has spent years explaining exactly how it works.",
    ]),
    dict(scene="proposals", text=[
        "Politicians have proposed fixes, like taxing unrealized gains of billionaires, or ending the step-up at death.",
        "So far, none of the big proposals have become law.",
    ]),
    dict(scene="risk", text=[
        "It's not risk free, though.",
        "If the stock crashes, the bank can demand more collateral. That's called a margin call, and it can force a sale at the worst possible moment.",
        "And since interest rates jumped in 2022, borrowing has become a lot more expensive than it was in the 2010s.",
    ]),
    # ---------- chapter 6 ----------
    dict(scene="lessons", args=dict(chap="6 · What you can actually use", n=0), text=[
        "So what can a normal person take from all this? More than you'd think.",
        "Lesson one: income is taxed hardest. Owning assets that grow is how wealth is built, even if you start small.",
    ]),
    dict(scene="lessons", args=dict(n=1), text=[
        "Lesson two: time matters. In the US, investments held more than a year are taxed at lower long-term rates, and for many people with lower incomes, that rate is zero.",
    ]),
    dict(scene="accounts", text=[
        "Lesson three: use the tax-advantaged accounts the system gives you.",
        "A 401(k) and a traditional IRA let you invest before tax. A Roth IRA lets your investments grow and come out tax free in retirement.",
        "That's your version of untaxed growth.",
    ]),
    dict(scene="lessons", args=dict(n=3), text=[
        "Lesson four: the step-up in basis isn't just for billionaires. It applies to a family home or a small stock portfolio too.",
        "And lesson five: borrowing against assets is a tool, not free money. Without a huge cushion, a market drop can wipe you out.",
    ]),
    dict(scene="outro", text=[
        "The rich don't follow different laws. They follow the same rules, but they know them better.",
        "So tell me in the comments: should the step-up in basis be ended, or is it fair? I read every one.",
        "Next time, we'll open another part of their playbook. Subscribe to The Quiet Money so you don't miss it.",
        "This video is for education only, and not financial advice.",
    ]),
]
SHORT = []
for _s in LONG:  # YouTube chapters = the on-screen chapter tags
    if _s.get("args", {}).get("chap"):
        _s["chapter"] = _s["args"]["chap"].split("· ")[-1]

def _i(name, k=0):
    return [i for i, sg in enumerate(LONG) if sg["scene"] == name][k]


SFX = [(_i("zero_tax"), "hit", 0.2), (_i("vs_teacher"), "pop", 1.2), (_i("rate_bars"), "pop", 4.0),
       (_i("zero_list"), "pop", 2.5), (_i("zero_list"), "pop", 6.0), (_i("zero_list"), "pop", 13.0),
       (_i("title"), "riser", 0.0), (_i("title"), "hit", 1.5), (_i("salary_vs_stock"), "ching", 6.0),
       (_i("need_cash"), "pop", 2.0), (_i("sell_tax"), "ching", 2.0), (_i("loan_not_income"), "hit", 0.4),
       (_i("loan_math"), "ching", 5.0), (_i("step_die"), "hit", 0.5), (_i("step_up"), "ching", 16.0),
       (_i("cycle"), "riser", 3.0), (_i("story"), "ching", 20.0), (_i("legal"), "hit", 0.6),
       (_i("risk"), "glitch", 4.0), (_i("outro"), "pop", 3.0)]


def thumb(S, c):
    S.thumbnail(c)

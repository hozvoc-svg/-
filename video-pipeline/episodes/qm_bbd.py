# The Quiet Money, episode 1: "Buy, Borrow, Die" (long-form, ~9-10 min).
# Facts: ProPublica "The Secret IRS Files" (June 2021); IRS/US tax code (37% top rate, 20% + 3.8% capital gains,
# step-up in basis, 40% estate tax, ~$15M exemption per person from 2026); Edward McCaffery (USC) coined the term.
SCENES_MODULE = "finance_scenes"
AMBIENT = "finance"
CAPTIONS = False
XFADE = 0.3
FADE = 0.001
GAP, TAIL = 0.3, 0.5
EL_VOICE = "UgBBYS2sOqTuMpoF3BR0"   # Mark: natural, conversational
EL_MODEL = "eleven_v3"              # most human-sounding model
EL_SETTINGS = dict(stability=0.5, similarity_boost=0.8)
FINAL = "x264"
PRON = {"401(k)": "four-oh-one-k", "IRS": "I R S", "ProPublica": "Pro Publica", "McCaffery": "Mc-Caffery",
        "$81,840": "eighty-one thousand, eight hundred and forty dollars"}

LONG = [
    # ---------- cold open ----------
    dict(scene="zero_tax", args=dict(year="2018"), text=[
        "So, in 2018, one of the richest people on Earth paid... zero dollars in federal income tax.",
        "Not a typo. Not a crime. Zero.",
    ]),
    dict(scene="vs_teacher", text=[
        "Now, that same year, a teacher making sixty thousand dollars paid roughly eleven thousand in federal income and payroll taxes.",
        "Taken straight out of every paycheck, before she ever saw a cent of it.",
    ]),
    dict(scene="rate_bars", text=[
        "And when journalists at ProPublica got their hands on leaked IRS data, they found something wild. The twenty-five richest Americans paid a true tax rate of just three point four percent.",
        "And the typical American household? Around fourteen percent.",
    ]),
    dict(scene="zero_list", text=[
        "And look, it's not just one guy, or one weird year.",
        "According to those same leaked records, Elon Musk paid zero in 2018.",
        "Jeff Bezos paid zero in 2007, and again in 2011. That year he even claimed a four thousand dollar tax credit... for his kids.",
        "Michael Bloomberg, Carl Icahn, George Soros. They all had years where they paid nothing, too.",
    ]),
    dict(scene="question", text=[
        "So how do people worth billions legally pay less than the people who teach their kids?",
        "Well, it comes down to a three-step playbook that tax lawyers have been using for decades.",
    ]),
    dict(scene="title", text=["It's called... Buy. Borrow. Die."]),
    # ---------- chapter 1 ----------
    dict(scene="two_money", args=dict(chap="1 · Two kinds of money"), text=[
        "Okay, to get this, you really only need to understand one thing about the tax system.",
        "It doesn't tax how rich you are. It taxes income.",
        "And here's the thing: there are two very different kinds of money.",
    ]),
    dict(scene="paycheck", text=[
        "The first one is income. Your salary, your wages, your bonus.",
        "And that money gets taxed automatically. Federal tax, state tax, social security, medicare.",
        "The government takes its cut before the money even hits your account. You don't even get a say.",
    ]),
    dict(scene="stock_grow", text=[
        "The second kind is wealth. Stuff you own that grows in value. Stocks, companies, real estate.",
        "So let's say your shares go from one million to one billion dollars. How much tax do you owe on that growth?",
        "Nothing. Not a single dollar.",
        "Until you sell, it's what's called an unrealized gain. And unrealized gains? They're not taxed.",
    ]),
    dict(scene="salary_vs_stock", text=[
        "And that's why the richest people often have weirdly small salaries.",
        "For years, Jeff Bezos's salary at Amazon was about $81,840. That's it.",
        "His real fortune was his stock. Worth well over a hundred billion dollars, just quietly growing... untaxed.",
    ]),
    # ---------- step 1 ----------
    dict(scene="step_buy", args=dict(chap="2 · Step one: Buy"), text=[
        "Which brings us to step one. Buy.",
        "You buy assets that grow. Shares of your own company, the stock market, buildings, land.",
    ]),
    dict(scene="never_sell", text=[
        "And then comes the most important rule of all. Never sell.",
        "Because selling is the moment your wealth turns into taxable income.",
        "As long as you hold, the IRS has nothing to tax. Nothing.",
    ]),
    dict(scene="need_cash", text=[
        "But, there's a problem.",
        "Billionaires have bills too. Houses, jets, staff, yachts.",
        "So if they never sell... where does the cash actually come from?",
    ]),
    dict(scene="sell_tax", text=[
        "See, selling stock would trigger capital gains tax. Up to twenty percent, plus another three point eight percent investment tax on top.",
        "On a billion-dollar sale? That's more than two hundred million dollars, just gone.",
        "So instead, they do something most people never even think about.",
    ]),
    # ---------- step 2 ----------
    dict(scene="borrow_bank", args=dict(chap="3 · Step two: Borrow"), text=[
        "Step two. Borrow.",
        "They walk into a bank and pledge their shares as collateral. Kind of like how your house backs a mortgage.",
        "And the bank just hands them cash. Millions. Sometimes hundreds of millions.",
    ]),
    dict(scene="loan_not_income", text=[
        "And this is the trick. A loan is not income.",
        "You have to pay it back, so the IRS doesn't tax it.",
        "Borrowed money shows up... completely tax free.",
    ]),
    dict(scene="loan_math", text=[
        "And honestly, for the very rich, the math is kind of beautiful.",
        "Say your portfolio is worth a hundred million dollars, and it grows seven percent a year. That's seven million.",
        "Now you borrow three million to live on, at four percent interest. That costs you about a hundred and twenty thousand dollars a year.",
        "So your wealth grows way faster than your debt. And you never paid income tax on any of it.",
    ]),
    dict(scene="filings", text=[
        "And this isn't some theory. It's right there in public company filings.",
        "Elon Musk has pledged huge amounts of Tesla stock to secure personal loans.",
        "Oracle's founder, Larry Ellison, has pledged Oracle shares to back his credit lines.",
    ]),
    dict(scene="rollover", text=[
        "And when a loan comes due? A lot of them just take out a new loan to pay off the old one.",
        "Borrow, roll it over, borrow again. For decades.",
        "Which takes us to the final step.",
    ]),
    dict(scene="scale", text=[
        "Oh, and can regular people do this? Kind of. A lot of brokers offer loans against your investments. It's usually called a securities-based line of credit.",
        "The difference is scale. Borrowing three percent of a fifty thousand dollar portfolio gets you... fifteen hundred bucks.",
        "But three percent of a hundred billion dollar fortune? That's three billion. Enough to live like royalty, forever.",
    ]),
    # ---------- step 3 ----------
    dict(scene="step_die", args=dict(chap="4 · Step three: Die"), text=[
        "Step three. Die.",
        "I know, it sounds dark. But this is where the biggest tax break of all is hiding.",
    ]),
    dict(scene="step_up", text=[
        "Imagine you bought shares for one million dollars, and by the time you die, they're worth one billion.",
        "Normally, selling them would mean paying tax on nine hundred and ninety-nine million dollars of profit.",
        "But when your heirs inherit those shares, the law resets their cost to today's value. One billion.",
        "It's called the step-up in basis. So if they sell the very next day, the taxable gain is... basically zero.",
        "Decades of growth. Never taxed as income. Ever.",
    ]),
    dict(scene="estate", text=[
        "Now, to be fair, there is an estate tax. Forty percent on fortunes above roughly fifteen million dollars per person.",
        "But the wealthy have armies of lawyers, and trusts that are built to shrink that bill. Sometimes dramatically.",
    ]),
    dict(scene="heirs_repay", text=[
        "So then the heirs sell a small slice of those stepped-up shares, pay off all the loans, and keep the rest.",
        "The debt is gone. And the tax on all that growth? It just never showed up.",
    ]),
    dict(scene="cycle", text=[
        "So, buy assets that grow. Borrow against them instead of selling. Hold them until you die, and pass them on with a fresh, stepped-up value.",
        "And that's how a fortune can keep growing for generations, while the income tax on it stays close to zero.",
        "No secret loophole. Just patience... and really good lawyers.",
    ]),
    dict(scene="story", args=dict(chap="Putting it together"), text=[
        "Alright, let's run the whole playbook on a made-up founder. Let's call him Alex.",
        "At thirty, Alex starts a company and keeps half of it. By fifty, his stake is worth five billion dollars. His salary? One dollar.",
        "Every year, he borrows fifty million against his shares to live on. Over thirty years, that's one and a half billion dollars of spending... and zero income tax.",
        "At eighty, Alex dies. His shares, now worth twenty billion, go to his kids with a stepped-up basis.",
        "They sell just enough to pay back the loans and the interest. Capital gains tax on that sale? Practically nothing.",
        "A whole lifetime of growth, twenty billion dollars, and almost no income tax was ever paid on it.",
    ]),
    # ---------- chapter 5 ----------
    dict(scene="legal", args=dict(chap="5 · Is this legal?"), text=[
        "So... is this legal? Yeah. Completely.",
        "The name Buy, Borrow, Die was popularized by USC law professor Edward McCaffery, who's spent years explaining exactly how it works.",
    ]),
    dict(scene="proposals", text=[
        "And politicians have pitched fixes. Like taxing billionaires' unrealized gains, or ending the step-up at death.",
        "But so far, none of the big proposals have actually become law.",
    ]),
    dict(scene="risk", text=[
        "That said, it's not risk free.",
        "If the stock crashes, the bank can demand more collateral. That's called a margin call, and it can force you to sell at the worst possible moment.",
        "And ever since interest rates jumped in 2022, borrowing has gotten a lot more expensive than it was back in the 2010s.",
    ]),
    # ---------- chapter 6 ----------
    dict(scene="lessons", args=dict(chap="6 · What you can actually use", n=0), text=[
        "So, what can a normal person actually take from all this? Honestly, more than you'd think.",
        "Lesson one. Income gets taxed the hardest. Owning assets that grow is how wealth gets built, even if you start small.",
    ]),
    dict(scene="lessons", args=dict(n=1), text=[
        "Lesson two. Time matters. In the US, investments you hold for more than a year get taxed at lower long-term rates. And for a lot of people with lower incomes, that rate is actually zero.",
    ]),
    dict(scene="accounts", text=[
        "Lesson three. Use the tax-advantaged accounts the system already gives you.",
        "A 401(k) and a traditional IRA let you invest before tax. And a Roth IRA lets your money grow and come out tax free in retirement.",
        "That's basically your version of untaxed growth.",
    ]),
    dict(scene="lessons", args=dict(n=3), text=[
        "Lesson four. The step-up in basis isn't just for billionaires. It applies to a family home, or a small stock portfolio too.",
        "And lesson five. Borrowing against your assets is a tool, not free money. Without a huge cushion, one bad market drop can wipe you out.",
    ]),
    dict(scene="outro", text=[
        "Look, the rich don't follow different laws. They follow the same rules. They just know them better.",
        "So let me know in the comments. Should the step-up in basis be ended, or is it fair? I read every single one.",
        "Next time, we're opening up another part of their playbook. So subscribe to The Quiet Money, so you don't miss it.",
        "And just so you know, this video is for education only. It's not financial advice.",
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

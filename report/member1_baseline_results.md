# Member 1 Baseline Benchmark (The Mom Test)

## Setup

- Source file: `The Mom Test.md`
- Strategy: Fixed-size 300 tokens, 10% overlap (30 tokens)
- Embedding backend: `text-embedding-3-small`
- top_k: `3`
- score_threshold: `0.7`
- Indexed chunks: `117`

## Results

| # | Query | Top-1 score | Top-1 chunk id | Above 0.7? | Relevant in top-3? |
|---|-------|-------------|----------------|------------|--------------------|
| 1 | Quy tắc cốt lõi của The Mom Test để tránh nhận lời nói dối là gì? | 0.3900 | momtest_chunk_0005::5 | no | yes |

### Query 1 details
- Gold answer: Nói về cuộc đời của họ thay vì ý tưởng của bạn; hỏi về các sự việc cụ thể trong quá khứ thay vì ý kiến tương lai; nói ít và lắng nghe nhiều.
- Top-1: score=0.3900, id=momtest_chunk_0005::5, preview=our responsibility to find it. W e do that by asking good questions. The Mom Test is a set of simple rules for crafting good questions that even your mom can't lie to you about. Before we get there, let's look at two conversations with mom ...
- Top-2: score=0.3785, id=momtest_chunk_0034::34, preview=The Mom Test to re-focus on the person, their life, and their goals. People rarely lie about specific stuff that's already happened, regardless of your ego. Some famous entrepreneurs don't suffer the effects of The Pathos Problem, but you s...
- Top-3: score=0.3567, id=momtest_chunk_0036::36, preview=their mental model of the world. Losing that learning is a shame. You'll have the chance to fill them in later. Plus, it's annoying to people if they start trying to help you and you cut them off to correct them. Rule of thumb: The more you...

| 2 | Tại sao những lời khen (compliments) lại được coi là vàng giả trong học hỏi khách hàng? | 0.4012 | momtest_chunk_0023::23 | no | yes |

### Query 2 details
- Gold answer: Vì lời khen thường là lịch sự xã giao, khiến founder ảo tưởng nhưng không cho dữ liệu hành vi đáng tin để ra quyết định.
- Top-1: score=0.4012, id=momtest_chunk_0023::23, preview=easy, but it's not. W e so desperately want to hear them that we are often tricked into registering them as positive data points instead of vacuous fibs. Sometimes it's easier to spot the symptoms than to notice the original compliment. ## ...
- Top-2: score=0.3613, id=momtest_chunk_0022::22, preview=learn about workflow inefficiencies and bumps. When I find one, I'll dig around that signal with more follow-ups. Them: (Even more workflow and alternate solution data) If we're early in the learning process, the meeting could end here quit...
- Top-3: score=0.3567, id=momtest_chunk_0020::20, preview=to deflect the compliment and get on with the business of gathering facts and commitments. Before we look at how to properly deflect compliments, here's what happens when you take them at face value: ## A bad conversation: - You: '…And that...

| 3 | Làm thế nào để neo giữ những thông tin mơ hồ từ khách hàng? | 0.3363 | momtest_chunk_0106::106 | no | no |

### Query 3 details
- Gold answer: Đặt câu hỏi neo vào ví dụ cụ thể trong quá khứ như lần gần nhất, hành động cụ thể, thay vì chấp nhận phát biểu chung chung.
- Top-1: score=0.3363, id=momtest_chunk_0106::106, preview=the pub, and on newspapers from the cafe. You'll want to transfer them over to your main storage system once you get back to the office, but it's better to capture what's said on something weird than to try to remember all the important bit...
- Top-2: score=0.3228, id=momtest_chunk_0096::96, preview=building interactive advertising products, I spent lots of time talking to guys in suits and very little (well, none) talking to the teenagers we were assuming would enjoy using our products. Telling my board that I had successfully talked ...
- Top-3: score=0.3200, id=momtest_chunk_0070::70, preview=discretionary budget to run a trial. Or who will fight for you against his boss and lawyers when they're saying the tech is unproven. In the consumer space, it's the fan who wants your product to succeed so badly that they'll front you the ...

| 4 | Dấu hiệu nào cho thấy một cuộc gặp khách hàng đã thành công (Advancement)? | 0.4510 | momtest_chunk_0061::61 | no | yes |

### Query 4 details
- Gold answer: Khách hàng đưa ra commitment rõ ràng như hẹn bước tiếp theo, giới thiệu đến người quyết định, hoặc cam kết trả tiền/đặt cọc.
- Top-1: score=0.4510, id=momtest_chunk_0061::61, preview=a consequence of being clingy and fearing rejection. By giving them a clear chance to either commit or reject us, we get out of the friend-zone and can identify the real leads. As always, you're not trying to convince every person to like w...
- Top-2: score=0.4357, id=momtest_chunk_0060::60, preview=to get to those 5 minutes. It can't be perfect every time. In the aforementioned case, we proved ourselves wrong. Sometimes, however, it goes in the opposite direction and everything we learn from customers makes us even more excited. In th...
- Top-3: score=0.4189, id=momtest_chunk_0113::113, preview=compliments, fluff, and opinions) - Commitment - They are showing they're serious by giving up something they value such as meaningful amounts of time, reputational risk, or money. - Advancement - They are moving to the next step of your re...

| 5 | Bạn nên làm gì khi lỡ tay thuyết trình về ý tưởng của mình quá sớm? | 0.2692 | momtest_chunk_0035::35 | no | yes |

### Query 5 details
- Gold answer: Cần dừng lại, xin lỗi, thừa nhận vừa pitch quá sớm và kéo cuộc trò chuyện trở lại vấn đề thực tế của khách hàng.
- Top-1: score=0.2692, id=momtest_chunk_0035::35, preview=in the first place. But suddenly, you find yourself five minutes into an enthusiastic monologue while the other person nods politely. That's bad. Once you start talking about your idea, they stop talking about their problems. Cut yourself o...
- Top-2: score=0.2416, id=momtest_chunk_0097::97, preview=extreme way to bottleneck is to go to the meetings alone and take crappy notes which you don't review with your team. At that point, your head has become the ultimate repository of customer truth and everyone just has to do what you say. In...
- Top-3: score=0.2391, id=momtest_chunk_0033::33, preview=brain dump. Rule of thumb: Ideas and feature requests should be understood, but not obeyed. ## Stop seeking approval As we've seen, compliments are dangerous and sneaky. So if we can nip them in the bud before they bloom, so much the better...

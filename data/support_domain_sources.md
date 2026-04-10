# Customer Support Domain - Recommended Sources

Tài liệu này tổng hợp các nguồn chính thống (official) cho domain Customer Support để dùng trong Lab Day 7.

## Cách dùng nhanh

- Không cần lấy toàn bộ nội dung trang web.
- Mỗi link chỉ cần trích phần nội dung cốt lõi và lưu thành file `.md` riêng trong `data/`.
- Mục tiêu là có 5-10 tài liệu cùng domain, có nguồn rõ ràng, phục vụ benchmark queries.

## Danh sách link + giải thích

1. **Atlassian Service Level Agreement (Legal)**
   - Link: [https://www.atlassian.com/legal/sla](https://www.atlassian.com/legal/sla)
   - Dùng cho: SLA chính thức, cam kết uptime, điều kiện áp dụng service credits.
   - Gợi ý metadata: `category=policy`, `doc_type=sla`, `source=atlassian`.

2. **Atlassian Cloud Products - SLA Guide**
   - Link: [https://support.atlassian.com/subscriptions-and-billing/docs/service-level-agreement-for-atlassian-cloud-products/](https://support.atlassian.com/subscriptions-and-billing/docs/service-level-agreement-for-atlassian-cloud-products/)
   - Dùng cho: quy trình vận hành liên quan SLA, điều kiện yêu cầu bồi hoàn, cách áp dụng thực tế.
   - Gợi ý metadata: `category=operations`, `doc_type=guide`, `source=atlassian_support`.

3. **Jira Service Management - SLA Overview**
   - Link: [https://confluence.atlassian.com/spaces/SERVICEMANAGEMENTSERVER0511/pages/1319568427/Service+Level+Agreements+SLAs+overview](https://confluence.atlassian.com/spaces/SERVICEMANAGEMENTSERVER0511/pages/1319568427/Service+Level+Agreements+SLAs+overview)
   - Dùng cho: định nghĩa metric SLA trong hệ thống helpdesk, cách cấu hình/chạy SLA.
   - Gợi ý metadata: `category=technical`, `doc_type=documentation`, `source=atlassian_docs`.

4. **Intercom - Best Practice Guide to Customer Support**
   - Link: [https://www.intercom.com/help/en/articles/198-our-best-practice-guide-to-customer-support](https://www.intercom.com/help/en/articles/198-our-best-practice-guide-to-customer-support)
   - Dùng cho: best practices tổng quan về support operations.
   - Gợi ý metadata: `category=support_ops`, `doc_type=best_practice`, `source=intercom`.

5. **Intercom - Best Practices Collection**
   - Link: [https://www.intercom.com/help/en/collections/3572492-best-practices](https://www.intercom.com/help/en/collections/3572492-best-practices)
   - Dùng cho: tập hợp nhiều bài con (dễ tách thành nhiều tài liệu nhỏ để benchmark).
   - Gợi ý metadata: `category=support_ops`, `doc_type=collection`, `source=intercom`.

6. **Zendesk - Customer Service Tone of Voice**
   - Link: [https://www.zendesk.com/blog/right-tone-of-voice/](https://www.zendesk.com/blog/right-tone-of-voice/)
   - Dùng cho: hướng dẫn phong cách giao tiếp, tone và phrasing cho đội support.
   - Gợi ý metadata: `category=communication`, `doc_type=guideline`, `source=zendesk`.

7. **Zendesk Help - AI Agent Tone-of-Voice Best Practices**
   - Link: [https://support.zendesk.com/hc/en-us/articles/8719119396506-Best-practices-for-using-instructions-and-custom-tone-of-voice-to-influence-advanced-AI-agent-responses](https://support.zendesk.com/hc/en-us/articles/8719119396506-Best-practices-for-using-instructions-and-custom-tone-of-voice-to-influence-advanced-AI-agent-responses)
   - Dùng cho: guideline dạng policy cho phản hồi AI/agent theo tone chuẩn.
   - Gợi ý metadata: `category=ai_support`, `doc_type=guideline`, `source=zendesk_support`.

8. **Freshdesk Support - Assignment Preferences**
   - Link: [https://support.freshdesk.com/support/solutions/articles/50000001699-configure-assignment-preferences](https://support.freshdesk.com/support/solutions/articles/50000001699-configure-assignment-preferences)
   - Dùng cho: ticket routing, queue assignment, triage workflow.
   - Gợi ý metadata: `category=triage`, `doc_type=workflow`, `source=freshdesk`.

## Gợi ý 6 file tối thiểu để bắt đầu

- `sla_atlassian.md`
- `sla_ops_guide_atlassian.md`
- `jsm_sla_overview.md`
- `intercom_support_best_practices.md`
- `zendesk_tone_of_voice.md`
- `freshdesk_ticket_routing.md`

Chỉ cần 6 file này là đã đủ tốt để nhóm chạy benchmark 5 queries theo rubric.

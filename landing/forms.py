from django import forms
from django.utils.translation import gettext_lazy as _

from .ax_tool_stack import (
    DIAGNOSIS_QUESTION_META,
    DIAGNOSIS_QUESTIONS,
    diagnosis_question_keys,
)


class ContactForm(forms.Form):
    HOME_INQUIRY_CHOICES = [
        ("coffee_chat", _("30분 무료 커피챗")),
        ("ax_diagnosis", _("자동화 실행 진단")),
        ("ax_build", _("자동화 실행 구축")),
        ("infra_setup", _("창업 기본 인프라 구축")),
        ("outsourcing", _("외주용역 집중 트랙")),
        ("other", _("기타")),
    ]
    FOREIGN_INQUIRY_CHOICES = [
        ("network", _("개발사 네트워크 연결")),
        ("career", _("취업/실무 커리어 상담")),
        ("settlement", _("정착/생활 연계 상담")),
        ("other", _("기타")),
    ]

    page_key = forms.CharField(
        required=False,
        initial="home",
        widget=forms.HiddenInput(),
    )
    lead_source = forms.CharField(
        required=False,
        initial="contact_form",
        widget=forms.HiddenInput(),
    )

    name = forms.CharField(
        label=_("이름"),
        max_length=50,
        widget=forms.TextInput(
            attrs={"placeholder": _("이름을 입력해 주세요"), "autocomplete": "name"}
        ),
    )
    company_name = forms.CharField(
        label=_("회사명"),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("회사명 (선택)")}),
    )
    contact = forms.CharField(
        label=_("연락 채널"),
        max_length=120,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": _("이메일 또는 LinkedIn 프로필 URL (선택)")}
        ),
    )
    email = forms.EmailField(
        label=_("이메일"),
        widget=forms.EmailInput(
            attrs={"placeholder": _("회신 받을 이메일"), "autocomplete": "email"}
        ),
    )
    inquiry_type = forms.ChoiceField(
        label=_("문의 유형"),
        choices=HOME_INQUIRY_CHOICES,
    )
    message = forms.CharField(
        label=_("문의 내용"),
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": _(
                    "프로젝트 목표, 예산 범위, 원하는 일정 등을 자유롭게 작성해 주세요."
                ),
            }
        ),
    )
    agree_privacy = forms.BooleanField(
        label=_("개인정보 수집 및 이용에 동의합니다."),
        error_messages={"required": _("문의 접수를 위해 동의가 필요합니다.")},
    )
    agree_marketing = forms.BooleanField(
        required=False,
        label=_("(선택) 자동화 진단/운영 팁 등 관련 정보 메일 수신에 동의합니다."),
    )
    agree_all = forms.BooleanField(
        required=False,
        label=_("전체 동의 (필수 + 선택)"),
    )

    def __init__(
        self,
        *args,
        page_key: str = "home",
        recommended_inquiry_type: str = "",
        lead_context: str = "",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.ui_copy = {
            "optional_note": _(
                "선택 동의는 문의 접수와 무관하며, 언제든 수신거부할 수 있습니다."
            ),
            "submit_label": _("문의 보내기"),
            "loading_message": _("처리 중입니다... 잠시만 기다려 주세요."),
            "response_sla": _("영업일 기준 1~2일 내 회신합니다."),
        }

        normalized_key = (
            page_key if page_key in {"home", "foreign_developers"} else "home"
        )
        self.fields["page_key"].initial = normalized_key
        self.fields["lead_source"].initial = (
            "foreign_developer_contact"
            if normalized_key == "foreign_developers"
            else "founder_contact"
        )
        if normalized_key == "home":
            self.fields["inquiry_type"].initial = "coffee_chat"

        if normalized_key == "foreign_developers":
            self.fields["inquiry_type"].choices = self.FOREIGN_INQUIRY_CHOICES
            self.fields["message"].widget.attrs["placeholder"] = _(
                "희망 직무/기술 스택, 현재 상황, 필요한 연결 지원을 작성해 주세요."
            )
            self.fields["agree_marketing"].label = _(
                "(선택) 외국인 개발자 커리어/네트워크 관련 정보 메일 수신에 동의합니다."
            )

        if lead_context == "lead_magnet_diagnosis" and normalized_key == "home":
            self.fields["lead_source"].initial = "founder_contact_from_diagnosis"

        if recommended_inquiry_type:
            choice_values = {value for value, _ in self.fields["inquiry_type"].choices}
            if recommended_inquiry_type in choice_values:
                self.fields["inquiry_type"].initial = recommended_inquiry_type


class ForeignQuickIntakeForm(forms.Form):
    nickname = forms.CharField(
        label="Nickname",
        max_length=50,
        widget=forms.TextInput(
            attrs={"placeholder": "Your name or nickname", "autocomplete": "name"}
        ),
    )
    email = forms.EmailField(
        label=_("이메일"),
        widget=forms.EmailInput(
            attrs={"placeholder": _("회신 받을 이메일"), "autocomplete": "email"}
        ),
    )
    target_role = forms.CharField(
        label="Target Role",
        max_length=80,
        widget=forms.TextInput(
            attrs={"placeholder": "e.g., Backend Engineer, AI Engineer"}
        ),
    )
    notes = forms.CharField(
        label="Anything you'd like to add (Optional)",
        required=False,
        max_length=300,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Share your current concerns, prep status, or preferred work style.",
            }
        ),
    )
    agree_privacy = forms.BooleanField(
        label=_("개인정보 수집 및 이용에 동의합니다."),
        error_messages={"required": _("문의 접수를 위해 동의가 필요합니다.")},
    )
    agree_marketing = forms.BooleanField(
        required=False,
        label=_(
            "(선택) 외국인 개발자 커리어/네트워크 관련 정보 메일 수신에 동의합니다."
        ),
    )
    join_community_waitlist = forms.BooleanField(
        required=False,
        label="(Optional) Join Community Waitlist updates",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui_copy = {
            "submit_label": "Get My Job Search Strategy",
            "helper": "2-minute quick intake. No resume required.",
            "loading_message": _("처리 중입니다... 잠시만 기다려 주세요."),
            "response_sla": _("영업일 기준 1~2일 내 회신합니다."),
        }


class ForeignMatchingProfileForm(forms.Form):
    email = forms.EmailField(
        label=_("이메일"),
        widget=forms.EmailInput(
            attrs={
                "placeholder": _("1차 등록에 사용한 이메일"),
                "autocomplete": "email",
            }
        ),
    )
    cv_or_linkedin = forms.CharField(
        label="CV or LinkedIn",
        max_length=300,
        widget=forms.TextInput(attrs={"placeholder": _("CV 링크 또는 LinkedIn URL")}),
    )
    github_or_portfolio = forms.CharField(
        label="GitHub or Portfolio",
        max_length=300,
        widget=forms.TextInput(attrs={"placeholder": _("GitHub/Portfolio URL")}),
    )
    tech_stack = forms.CharField(
        label="Tech Stack",
        max_length=200,
        widget=forms.TextInput(
            attrs={"placeholder": _("예: Python, Django, React, AWS")}
        ),
    )
    experience_level = forms.CharField(
        label="Experience Level",
        max_length=60,
        widget=forms.TextInput(attrs={"placeholder": _("예: 3 years, Mid-level")}),
    )
    visa_status = forms.CharField(
        label="Visa / Stay Status",
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": _("예: D-10, F-2, E-7 준비 중")}),
    )
    work_preference = forms.CharField(
        label="Work Preference",
        max_length=120,
        widget=forms.TextInput(
            attrs={"placeholder": _("예: Full-time, Hybrid, Remote")}
        ),
    )
    location_preference = forms.CharField(
        label="Location Preference",
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": _("예: Seoul, Gwangju")}),
    )
    available_from = forms.CharField(
        label="Available From",
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": _("예: Immediately, 2026-06")}),
    )
    agree_privacy = forms.BooleanField(
        label=_("개인정보 수집 및 이용에 동의합니다."),
        error_messages={"required": _("문의 접수를 위해 동의가 필요합니다.")},
    )
    join_community_waitlist = forms.BooleanField(
        required=False,
        label="(Optional) Join Community Waitlist updates",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui_copy = {
            "submit_label": "Complete My Matching Profile",
            "helper": "Add profile details for matching review.",
            "loading_message": _("처리 중입니다... 잠시만 기다려 주세요."),
        }


class ForeignCommunityWaitlistForm(forms.Form):
    email = forms.EmailField(
        label=_("이메일"),
        widget=forms.EmailInput(
            attrs={"placeholder": _("커뮤니티 대기열 안내를 받을 이메일")}
        ),
    )
    note = forms.CharField(
        label="Topic you'd like to share (Optional)",
        required=False,
        max_length=240,
        widget=forms.TextInput(
            attrs={"placeholder": _("예: 면접 준비, 한국어 학습, 비자 준비 경험")}
        ),
    )
    agree_privacy = forms.BooleanField(
        label=_("개인정보 수집 및 이용에 동의합니다."),
        error_messages={"required": _("문의 접수를 위해 동의가 필요합니다.")},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui_copy = {
            "submit_label": "Join Community Waitlist",
            "helper": "Community channel opens after operational threshold is reached.",
            "loading_message": _("처리 중입니다... 잠시만 기다려 주세요."),
        }


class LeadMagnetForm(forms.Form):
    SCORE_CHOICES = [
        ("0", "하고 있지 않음"),
        ("1", "어느 정도 하고 있음"),
        ("2", "명확히 하고 있음"),
    ]

    lead_source = forms.CharField(
        required=False,
        initial="founder_lead_magnet",
        widget=forms.HiddenInput(),
    )
    name = forms.CharField(
        label="이름",
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "이름"}),
    )
    email = forms.EmailField(
        label="이메일",
        widget=forms.EmailInput(attrs={"placeholder": "리포트 수신 이메일"}),
    )
    company_name = forms.CharField(
        label="회사명",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "회사명 (선택)"}),
    )
    agree_privacy = forms.BooleanField(
        label="개인정보 수집 및 이용에 동의합니다.",
        error_messages={"required": "리포트 제공을 위해 동의가 필요합니다."},
    )
    agree_marketing = forms.BooleanField(
        required=False,
        label="(선택) 자동화 실행 진단/운영 가이드 메일 수신에 동의합니다.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for question_key in diagnosis_question_keys():
            question_meta = DIAGNOSIS_QUESTION_META[question_key]
            self.fields[question_key] = forms.ChoiceField(
                label=DIAGNOSIS_QUESTIONS[question_key],
                choices=self.SCORE_CHOICES,
                widget=forms.RadioSelect(),
                required=bool(question_meta["required"]),
            )


class TestimonialSubmissionForm(forms.Form):
    name = forms.CharField(
        label="이름",
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "이름 또는 이니셜"}),
    )
    role_title = forms.CharField(
        label="직무/역할",
        max_length=80,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "예: 대표, 운영 매니저 (선택)"}),
    )
    company_name = forms.CharField(
        label="회사명",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "회사명 (선택)"}),
    )
    content = forms.CharField(
        label="후기 내용",
        widget=forms.Textarea(
            attrs={
                "rows": 6,
                "placeholder": "상담에서 특히 도움이 된 점과 실행 변화 계획을 적어 주세요.",
            }
        ),
    )

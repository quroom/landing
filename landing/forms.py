from django import forms
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from .ax_tool_stack import (
    DIAGNOSIS_QUESTION_META,
    DIAGNOSIS_QUESTIONS,
    diagnosis_question_keys,
)


class ContactForm(forms.Form):
    ALLOWED_PAGE_KEYS = {
        "home",
        "foreign_developers",
        "gwangju",
        "gwangju_homepage",
        "gwangju_web_development",
        "gwangju_app_development",
        "outsourcing_checklist",
    }
    GWANGJU_PAGE_KEYS = {
        "gwangju",
        "gwangju_homepage",
        "gwangju_web_development",
        "gwangju_app_development",
        "outsourcing_checklist",
    }
    HOME_INQUIRY_CHOICES = [
        ("coffee_chat", _("30분 무료 커피챗")),
        ("ax_diagnosis", _("자동화 실행 진단")),
        ("ax_build", _("자동화 실행 구축")),
        ("infra_setup", _("창업 기본 인프라 구축")),
        ("outsourcing", _("외주용역 집중 트랙")),
        ("other", _("기타")),
    ]
    GWANGJU_INQUIRY_CHOICES = [
        ("gwangju_scope", _("프로젝트 범위/견적 정리")),
        ("gwangju_homepage", _("광주 홈페이지 제작")),
        ("gwangju_web", _("광주 웹개발")),
        ("gwangju_app", _("광주 앱개발")),
        ("outsourcing_check", _("외주 전 체크리스트 점검")),
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

        normalized_key = page_key if page_key in self.ALLOWED_PAGE_KEYS else "home"
        self.fields["page_key"].initial = normalized_key
        if normalized_key == "foreign_developers":
            self.fields["lead_source"].initial = "foreign_developer_contact"
        elif normalized_key in self.GWANGJU_PAGE_KEYS:
            self.fields["lead_source"].initial = "gwangju_contact"
            self.fields["inquiry_type"].choices = self.GWANGJU_INQUIRY_CHOICES
            self.fields["inquiry_type"].initial = "gwangju_scope"
            self.fields["message"].widget.attrs["placeholder"] = _(
                "필요한 페이지/기능, 현재 준비된 자료, 예산 범위, 원하는 일정을 작성해 주세요."
            )
            self.fields["agree_marketing"].label = _(
                "(선택) 광주 홈페이지/웹개발/외주 체크리스트 관련 정보 메일 수신에 동의합니다."
            )
        else:
            self.fields["lead_source"].initial = "founder_contact"
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

    def clean_page_key(self) -> str:
        page_key = (self.cleaned_data.get("page_key") or "").strip()
        if page_key in self.ALLOWED_PAGE_KEYS:
            return page_key
        return "home"


def _is_korean_locale() -> bool:
    return (get_language() or "ko").split("-")[0] == "ko"


def _set_field_copy(
    field: forms.Field,
    *,
    label: str,
    placeholder: str | None = None,
) -> None:
    field.label = label
    if placeholder is not None and hasattr(field.widget, "attrs"):
        field.widget.attrs["placeholder"] = placeholder


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
        label="Current Focus or Role",
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "placeholder": "e.g., Software Engineer, Designer, Student, Researcher"
            }
        ),
    )
    notes = forms.CharField(
        label="Anything you'd like to add (Optional)",
        required=False,
        max_length=300,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Share what you are preparing for in Korea, your current concerns, or your preferred work style.",
            }
        ),
    )
    agree_privacy = forms.BooleanField(
        label=_("개인정보 수집 및 이용에 동의합니다."),
        error_messages={"required": _("문의 접수를 위해 동의가 필요합니다.")},
    )
    agree_marketing = forms.BooleanField(
        required=False,
        label=_("(선택) 한국 취업/커뮤니티 관련 정보 메일 수신에 동의합니다."),
    )
    join_community_waitlist = forms.BooleanField(
        required=False,
        label="(Optional) Join International Talent Community Waitlist",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if _is_korean_locale():
            _set_field_copy(
                self.fields["nickname"],
                label="이름 또는 닉네임",
                placeholder="이름 또는 닉네임",
            )
            _set_field_copy(
                self.fields["email"],
                label="이메일",
                placeholder="회신 받을 이메일",
            )
            _set_field_copy(
                self.fields["target_role"],
                label="현재 역할 또는 관심 분야",
                placeholder="예: 소프트웨어 엔지니어, 디자이너, 학생, 연구자",
            )
            _set_field_copy(
                self.fields["notes"],
                label="추가로 전하고 싶은 내용 (선택)",
                placeholder="한국에서 준비 중인 일, 현재 고민, 원하는 일 방식 등을 적어주세요.",
            )
            self.fields["agree_privacy"].label = "개인정보 수집 및 이용에 동의합니다."
            self.fields["agree_privacy"].error_messages["required"] = (
                "문의 접수를 위해 동의가 필요합니다."
            )
            self.fields[
                "agree_marketing"
            ].label = "(선택) 한국 취업/커뮤니티 관련 정보 메일 수신에 동의합니다."
            self.fields[
                "join_community_waitlist"
            ].label = "(선택) 글로벌 인재 커뮤니티 대기열에 참여합니다."
            self.ui_copy = {
                "submit_label": "문의 보내기",
                "helper": "1~2분 정도면 됩니다. 현재 상황이나 방향을 간단히 남겨주세요.",
                "loading_message": "처리 중입니다... 잠시만 기다려 주세요.",
                "response_sla": "영업일 기준 1~2일 내 회신합니다.",
            }
            return

        _set_field_copy(
            self.fields["nickname"],
            label="Name or Nickname",
            placeholder="Your name or nickname",
        )
        _set_field_copy(
            self.fields["email"],
            label="Email",
            placeholder="Email for reply",
        )
        _set_field_copy(
            self.fields["target_role"],
            label="Current Focus or Role",
            placeholder="e.g., Software Engineer, Designer, Student, Researcher",
        )
        _set_field_copy(
            self.fields["notes"],
            label="Anything you'd like to add (Optional)",
            placeholder="Share what you are preparing for in Korea, your current concerns, or your preferred work style.",
        )
        self.fields[
            "agree_privacy"
        ].label = "I agree to the collection and use of personal information."
        self.fields["agree_privacy"].error_messages["required"] = (
            "Consent is required to submit your inquiry."
        )
        self.fields[
            "agree_marketing"
        ].label = "(Optional) I agree to receive email updates about jobs or community support in Korea."
        self.fields[
            "join_community_waitlist"
        ].label = "(Optional) Join the international talent community waitlist"
        self.ui_copy = {
            "submit_label": "Send Inquiry",
            "helper": "Takes 1-2 minutes. Share your current direction in Korea.",
            "loading_message": "Processing... please wait.",
            "response_sla": "We usually reply within 1-2 business days.",
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
        label="(Optional) Join International Talent Community Waitlist",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if _is_korean_locale():
            _set_field_copy(
                self.fields["email"],
                label="이메일",
                placeholder="1단계 등록에 사용한 이메일",
            )
            _set_field_copy(
                self.fields["cv_or_linkedin"],
                label="CV 또는 LinkedIn",
                placeholder="CV 링크 또는 LinkedIn URL",
            )
            _set_field_copy(
                self.fields["github_or_portfolio"],
                label="GitHub 또는 포트폴리오",
                placeholder="GitHub 또는 포트폴리오 URL",
            )
            _set_field_copy(
                self.fields["tech_stack"],
                label="기술 스택",
                placeholder="예: Python, Django, React, AWS",
            )
            _set_field_copy(
                self.fields["experience_level"],
                label="경력 수준",
                placeholder="예: 3 years, Mid-level",
            )
            _set_field_copy(
                self.fields["visa_status"],
                label="비자 / 체류 상태",
                placeholder="예: D-10, F-2, E-7 준비 중",
            )
            _set_field_copy(
                self.fields["work_preference"],
                label="희망 근무 형태",
                placeholder="예: Full-time, Hybrid, Remote",
            )
            _set_field_copy(
                self.fields["location_preference"],
                label="희망 지역",
                placeholder="예: Seoul, Gwangju",
            )
            _set_field_copy(
                self.fields["available_from"],
                label="가능 시작 시점",
                placeholder="예: Immediately, 2026-06",
            )
            self.fields["agree_privacy"].label = "개인정보 수집 및 이용에 동의합니다."
            self.fields["agree_privacy"].error_messages["required"] = (
                "문의 접수를 위해 동의가 필요합니다."
            )
            self.fields[
                "join_community_waitlist"
            ].label = "(선택) 글로벌 인재 커뮤니티 대기열에 참여합니다."
            self.ui_copy = {
                "submit_label": "프로필 제출하기",
                "helper": "외국인 소프트웨어 엔지니어이거나 관련 진로를 준비 중인 분께 가장 적합합니다.",
                "loading_message": "처리 중입니다... 잠시만 기다려 주세요.",
            }
            return

        _set_field_copy(
            self.fields["email"],
            label="Email",
            placeholder="Email used in Step 1",
        )
        _set_field_copy(
            self.fields["cv_or_linkedin"],
            label="CV or LinkedIn",
            placeholder="CV link or LinkedIn URL",
        )
        _set_field_copy(
            self.fields["github_or_portfolio"],
            label="GitHub or Portfolio",
            placeholder="GitHub or portfolio URL",
        )
        _set_field_copy(
            self.fields["tech_stack"],
            label="Tech Stack",
            placeholder="e.g., Python, Django, React, AWS",
        )
        _set_field_copy(
            self.fields["experience_level"],
            label="Experience Level",
            placeholder="e.g., 3 years, Mid-level",
        )
        _set_field_copy(
            self.fields["visa_status"],
            label="Visa / Stay Status",
            placeholder="e.g., D-10, F-2, Preparing for E-7",
        )
        _set_field_copy(
            self.fields["work_preference"],
            label="Work Preference",
            placeholder="e.g., Full-time, Hybrid, Remote",
        )
        _set_field_copy(
            self.fields["location_preference"],
            label="Location Preference",
            placeholder="e.g., Seoul, Gwangju",
        )
        _set_field_copy(
            self.fields["available_from"],
            label="Available From",
            placeholder="e.g., Immediately, 2026-06",
        )
        self.fields[
            "agree_privacy"
        ].label = "I agree to the collection and use of personal information."
        self.fields["agree_privacy"].error_messages["required"] = (
            "Consent is required to submit your inquiry."
        )
        self.fields[
            "join_community_waitlist"
        ].label = "(Optional) Join the international talent community waitlist"
        self.ui_copy = {
            "submit_label": "Submit My Profile",
            "helper": "Best for foreign software engineers ready for practical review.",
            "loading_message": "Processing... please wait.",
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
        if _is_korean_locale():
            _set_field_copy(
                self.fields["email"],
                label="이메일",
                placeholder="커뮤니티 소식을 받을 이메일",
            )
            _set_field_copy(
                self.fields["note"],
                label="나누고 싶은 주제 (선택)",
                placeholder="예: 면접 준비, 한국어 학습, 비자 준비 경험",
            )
            self.fields["agree_privacy"].label = "개인정보 수집 및 이용에 동의합니다."
            self.fields["agree_privacy"].error_messages["required"] = (
                "문의 접수를 위해 동의가 필요합니다."
            )
            self.ui_copy = {
                "submit_label": "커뮤니티 대기열 신청",
                "helper": "더 넓은 외국인 인재도 참여할 수 있으며, 운영 기준이 갖춰지면 순차적으로 안내합니다.",
                "loading_message": "처리 중입니다... 잠시만 기다려 주세요.",
            }
            return

        _set_field_copy(
            self.fields["email"],
            label="Email",
            placeholder="Email for community updates",
        )
        _set_field_copy(
            self.fields["note"],
            label="Topic you'd like to share (Optional)",
            placeholder="e.g., interview prep, learning Korean, visa experience",
        )
        self.fields[
            "agree_privacy"
        ].label = "I agree to the collection and use of personal information."
        self.fields["agree_privacy"].error_messages["required"] = (
            "Consent is required to submit your inquiry."
        )
        self.ui_copy = {
            "submit_label": "Join Community Waitlist",
            "helper": "Open to broader international talent. The live channel opens after the operating threshold is reached.",
            "loading_message": "Processing... please wait.",
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

from django import forms

from .ax_tool_stack import DIAGNOSIS_QUESTIONS, diagnosis_question_keys


class ContactForm(forms.Form):
    HOME_INQUIRY_CHOICES = [
        ("development", "서비스 개발"),
        ("matching", "외국인 개발자 연계"),
        ("outsourcing", "고액 외주 상담"),
        ("other", "기타"),
    ]
    FOREIGN_INQUIRY_CHOICES = [
        ("network", "개발사 네트워크 연결"),
        ("career", "취업/실무 커리어 상담"),
        ("settlement", "정착/생활 연계 상담"),
        ("other", "기타"),
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
        label="이름",
        max_length=50,
        widget=forms.TextInput(
            attrs={"placeholder": "이름을 입력해 주세요", "autocomplete": "name"}
        ),
    )
    company_name = forms.CharField(
        label="회사명",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "회사명 (선택)"}),
    )
    contact = forms.CharField(
        label="연락 채널",
        max_length=120,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "이메일 또는 LinkedIn 프로필 URL (선택)"}
        ),
    )
    email = forms.EmailField(
        label="이메일",
        widget=forms.EmailInput(
            attrs={"placeholder": "회신 받을 이메일", "autocomplete": "email"}
        ),
    )
    inquiry_type = forms.ChoiceField(
        label="문의 유형",
        choices=HOME_INQUIRY_CHOICES,
    )
    message = forms.CharField(
        label="문의 내용",
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "프로젝트 목표, 예산 범위, 원하는 일정 등을 자유롭게 작성해 주세요.",
            }
        ),
    )
    agree_privacy = forms.BooleanField(
        label="개인정보 수집 및 이용에 동의합니다.",
        error_messages={"required": "문의 접수를 위해 동의가 필요합니다."},
    )
    agree_marketing = forms.BooleanField(
        required=False,
        label="(선택) 자동화 진단/운영 팁 등 관련 정보 메일 수신에 동의합니다.",
    )
    agree_all = forms.BooleanField(
        required=False,
        label="전체 동의 (필수 + 선택)",
    )

    def __init__(self, *args, page_key: str = "home", **kwargs):
        super().__init__(*args, **kwargs)
        normalized_key = (
            page_key if page_key in {"home", "foreign_developers"} else "home"
        )
        self.fields["page_key"].initial = normalized_key
        self.fields["lead_source"].initial = (
            "foreign_developer_contact"
            if normalized_key == "foreign_developers"
            else "founder_contact"
        )

        if normalized_key == "foreign_developers":
            self.fields["inquiry_type"].choices = self.FOREIGN_INQUIRY_CHOICES
            self.fields["message"].widget.attrs[
                "placeholder"
            ] = "희망 직무/기술 스택, 현재 상황, 필요한 연결 지원을 작성해 주세요."
            self.fields["agree_marketing"].label = (
                "(선택) 외국인 개발자 커리어/네트워크 관련 정보 메일 수신에 동의합니다."
            )


class LeadMagnetForm(forms.Form):
    SCORE_CHOICES = [
        ("0", "해당 없음"),
        ("1", "일부 해당"),
        ("2", "강하게 해당"),
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
            self.fields[question_key] = forms.ChoiceField(
                label=DIAGNOSIS_QUESTIONS[question_key],
                choices=self.SCORE_CHOICES,
                widget=forms.RadioSelect(),
            )

from django.db import models

# 応募者テーブル
class Applicant(models.Model):
    # IDは自動的に Django が作成する
    application_date = models.DateField(verbose_name="応募日")
    name = models.CharField(max_length=100, verbose_name="氏名")
    application_route = models.CharField(max_length=100, verbose_name="応募経路")
    
    casual_meeting_date = models.DateField(null=True, blank=True, verbose_name="カジュアル面談実施日")
    
    document_selection_pass_date = models.DateField(null=True, blank=True, verbose_name="書類選考通過日")

    first_interview_date = models.DateField(null=True, blank=True, verbose_name="1次面接実施日")
    first_interview_note = models.TextField(null=True, blank=True, verbose_name="1次面接メモ")

    second_interview_date = models.DateField(null=True, blank=True, verbose_name="2次面接実施日")
    second_interview_note = models.TextField(null=True, blank=True, verbose_name="2次面接メモ")

    offer_date = models.DateField(null=True, blank=True, verbose_name="内定通知日")
    offer_note = models.TextField(null=True, blank=True, verbose_name="内定通知メモ")

    offer_acceptance_date = models.DateField(null=True, blank=True, verbose_name="内定承諾日")
    offer_acceptance_note = models.TextField(null=True, blank=True, verbose_name="内定承諾メモ")

    job_position = models.CharField(max_length=100, verbose_name="募集職種")
    age = models.IntegerField(verbose_name="年齢")
    region = models.CharField(max_length=100, verbose_name="地域")
    skills = models.TextField(verbose_name="スキル")
    desired_joining_date = models.DateField(null=True, blank=True, verbose_name="入社希望時期")
    
    current_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="現年収")
    desired_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="希望年収")
    offered_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="提示金額")
    
    memo = models.TextField(null=True, blank=True, verbose_name="メモ")

    # 選考フェーズの選択肢
    SELECTION_PHASE_CHOICES = [
        (0, '応募'),
        (1, '書類選考'),
        (2, '1次面接'),
        (3, '2次面接'),
        (4, '内定'),
    ]

    # 選考ステータスの選択肢
    SELECTION_STATUS_CHOICES = [
        (0, '未処理'),
        (1, '選考OK'),
        (2, '選考NG'),
        (3, '調整中'),
        (4, '日程確定'),
        (5, '内定通知'),
        (6, '内定承諾'),
        (7, '入社'),
        (8, '辞退'),
    ]

    selection_phase = models.IntegerField(choices=SELECTION_PHASE_CHOICES, default=0, verbose_name="選考フェーズ")
    selection_status = models.IntegerField(choices=SELECTION_STATUS_CHOICES, default=0, verbose_name="選考ステータス")

    def __str__(self):
        return self.name
    
# 採用費テーブル
class RecruitmentCost(models.Model):
    date = models.DateField(verbose_name="費用発生日")
    description = models.CharField(max_length=255, verbose_name="費用の内容")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="費用額（円）")

    def __str__(self):
        return f"{self.date} - {self.description}: {self.amount}円"

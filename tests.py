from django.db import models
import pytest

from registrable.choices import DynamicLazyChoices, ModelLazyChoices


@pytest.mark.unit
def test_dynamiclazychoices_register():
    choices = DynamicLazyChoices()
    a_group_name = 'A Choice Group Name'
    a_choice_value = 'a_choice_value'
    a_choice_label = 'A Choice Label to Display'
    expected = a_choice = (
        a_group_name, (
            (a_choice_value, a_choice_label),
        ),
    )

    uut = choices.register
    uut(*a_choice)

    assert expected in choices


@pytest.mark.unit
def test_dynamiclazychoices_is_group_choice():
    choices = DynamicLazyChoices()
    a_group_name = 'A Choice Group Name'
    a_choice_value = 'a_choice_value'
    a_choice_label = 'A Choice Label to Display'
    a_choice = (
        a_group_name, (
            (a_choice_value, a_choice_label),
        ),
    )
    expected = True

    uut = choices.is_group_choice
    result = uut(a_choice)

    assert expected == result


@pytest.mark.unit
def test_dynamiclazychoices_get_group():
    choices = DynamicLazyChoices()
    a_group_name = 'A Choice Group Name'
    a_choice_value = 'a_choice_value'
    a_choice_label = 'A Choice Label to Display'
    a_group_choice = (
        a_group_name, (
            (a_choice_value, a_choice_label),
        ),
    )
    another_group_choice = (
        a_group_name, (
            (a_choice_value, a_choice_label),
        ),
    )
    a_choice = (a_choice_value, a_choice_label)
    choices.register(*a_group_choice)
    choices.register(*another_group_choice)
    choices.register(*a_choice)
    expected = (
        a_group_name, (
            (a_choice_value, a_choice_label),
            (a_choice_value, a_choice_label),
        ),
    )

    uut = choices.get_group
    result = uut(a_group_name)

    assert expected == result


@pytest.mark.unit
def test_dynamiclazychoices_get_group_without_choices():
    choices = DynamicLazyChoices()
    a_group_name = 'whathever'
    expected = None

    uut = choices.get_group
    result = uut(a_group_name)

    assert expected == result


@pytest.mark.unit
def test_dynamiclazychoices_get_group_with_only_ungrouped_choices():
    choices = DynamicLazyChoices()
    a_group_name = 'whathever'
    a_choice_value = 'a_choice_value'
    a_choice_label = 'A Choice Label to Display'
    a_choice = (a_choice_value, a_choice_label),
    choices.register(*a_choice)
    expected = None

    uut = choices.get_group
    result = uut(a_group_name)

    assert expected == result


@pytest.mark.unit
def test_dynamiclazychoices_get_group_for_invalid_group_name():
    choices = DynamicLazyChoices()
    an_invalid_group_name = 'whathever'
    a_group_name = 'A Choice Group Name'
    a_choice_value = 'a_choice_value'
    a_choice_label = 'A Choice Label to Display'
    a_group_choice = (
        a_group_name, (
            (a_choice_value, a_choice_label),
        ),
    )
    choices.register(*a_group_choice)
    expected = None

    uut = choices.get_group
    result = uut(an_invalid_group_name)

    assert expected == result


@pytest.mark.unit
def test_dynamiclazychoices_equals_should_be_false_when_a_non_iterable():
    choices = DynamicLazyChoices()
    a_non_iterable_object = 0
    expected = False

    result = choices == a_non_iterable_object
    assert expected == result

    result = a_non_iterable_object == choices
    assert expected == result


@pytest.mark.skip
@pytest.mark.unit
def test_dynamiclazychoices_raise_check_error():
    pass


@pytest.mark.unit
def test_modellazychoices_functor_decorator_register():
    model_choices = ModelLazyChoices()
    expected = (
        ('ModelA', 'Model A'),
        ('mB', 'M - B'),
        ('custom_m_C', 'Custom Model C'),
        (
            'A Choices Group', (
                ('group_choice_a', 'A Choice Inside a Group'),
                ('group_choice_b', 'Another Choice Inside a Group'),
            ),
        ),
    )

    @model_choices
    class ModelA(models.Model):
        class Meta:
            verbose_name = 'Model A'
            abstract = True

    @model_choices
    class ModelB(models.Model):
        _choice_value = 'mB'
        _choice_label = 'M - B'

        class Meta:
            abstract = True

    @model_choices(value_attr='_value', label_attr='_display')
    class ModelC(models.Model):
        _value = 'custom_m_C'
        _display = 'Custom Model C'

        class Meta:
            abstract = True

    @model_choices
    class ModelD(models.Model):
        _choice_group = 'A Choices Group'
        _choice_value = 'group_choice_a'
        _choice_label = 'A Choice Inside a Group'

        class Meta:
            abstract = True

    @model_choices(group_attr='_group')
    class ModelE(models.Model):
        _group = 'A Choices Group'
        _choice_value = 'group_choice_b'
        _choice_label = 'Another Choice Inside a Group'

        class Meta:
            abstract = True

    assert expected == model_choices


@pytest.mark.unit
def test_modellazychoices_register():
    model_choices = ModelLazyChoices()
    expected = (
        ('ModelA', 'Model A'),
        ('mB', 'M - B'),
        ('custom_m_C', 'Custom Model C'),
        (
            'A Choices Group', (
                ('group_choice_a', 'A Choice Inside a Group'),
                ('group_choice_b', 'Another Choice Inside a Group'),
            ),
        ),
    )

    class ModelA(models.Model):
        class Meta:
            verbose_name = 'Model A'
            abstract = True

    model_choices.register(ModelA)

    class ModelB(models.Model):
        _choice_value = 'mB'
        _choice_label = 'M - B'

        class Meta:
            abstract = True

    model_choices.register(ModelB)

    class ModelC(models.Model):
        _value = 'custom_m_C'
        _display = 'Custom Model C'

        class Meta:
            abstract = True

    model_choices.register(ModelC, value_attr='_value', label_attr='_display')

    class ModelD(models.Model):
        _choice_group = 'A Choices Group'
        _choice_value = 'group_choice_a'
        _choice_label = 'A Choice Inside a Group'

        class Meta:
            abstract = True

    model_choices.register(ModelD)

    class ModelE(models.Model):
        _group = 'A Choices Group'
        _choice_value = 'group_choice_b'
        _choice_label = 'Another Choice Inside a Group'

        class Meta:
            abstract = True

    model_choices(ModelE, group_attr='_group')

    assert expected == model_choices


@pytest.mark.unit
def test_modellazychoices_get_model_for_valid_choice_value():
    model_choices = ModelLazyChoices()

    class ModelA(models.Model):
        _choice_value = 'a'
        _choice_label = 'A'

        class Meta:
            verbose_name = 'Model A'
            abstract = True

    a_valid_choice_value = ModelA._choice_value
    expected = ModelA

    model_choices.register(ModelA)

    assert expected == model_choices.get_model(a_valid_choice_value)


@pytest.mark.unit
def test_modellazychoices_get_model_for_invalid_choice_value():
    model_choices = ModelLazyChoices()

    class ModelA(models.Model):
        _choice_value = 'a'
        _choice_label = 'A'

        class Meta:
            verbose_name = 'Model A'
            abstract = True

    an_invalid_choice_value = 'invalid choice value'
    expected = None

    model_choices.register(ModelA)

    assert expected == model_choices.get_model(an_invalid_choice_value)

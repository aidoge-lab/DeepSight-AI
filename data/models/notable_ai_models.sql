-- AI Models Database Schema
-- This table stores information about notable AI models and their characteristics
-- Based on the notable_ai_models.csv dataset

CREATE TABLE ai_models (
    -- Model identification
    model VARCHAR(255) NOT NULL,
    -- The name of the AI model
    -- Examples: "GPT-4.5", "Claude 3.7 Sonnet", "Llama 4 Behemoth (preview)"
    
    organization VARCHAR(500),
    -- The organization(s) that developed the model
    -- Examples: "OpenAI", "Google DeepMind", "NVIDIA,Nanjing University,Tsinghua University"
    
    publication_date DATE,
    -- The date when the model was published or announced
    -- Examples: "2025-05-21", "2025-02-27", "2025-01-20"
    
    -- Model capabilities and domain
    domain TEXT,
    -- The primary domain(s) the model is designed for
    -- Examples: "Language,Vision,Multimodal", "Video,Vision", "Mathematics"
    
    task TEXT,
    -- Specific tasks the model can perform
    -- Examples: "Language modeling/generation,Question answering,Code generation", "Video generation,Image-to-video"
    
    -- Model architecture details
    parameters BIGINT,
    -- Number of parameters in the model (numeric value)
    -- Examples: 135000000000 (135B), 32000000000 (32B), 7000000000 (7B)
    
    parameters_notes TEXT,
    -- Additional notes about the parameters
    -- Examples: "32B", "Architecture: transformers with RoPE, SwiGLU, RMSNorm"
    
    -- Training compute information
    training_compute_flop DECIMAL(30,10),
    -- Training compute in FLOP (Floating Point Operations)
    -- Examples: 1.0692e+25, 3.51e+24, 4.7156e+22
    
    training_compute_notes TEXT,
    -- Additional notes about training compute calculations
    -- Examples: "6*135000000000*13200000000000=1.069200e+25", "Assuming the same dataset size as for Qwen2.5 training"
    
    -- Training dataset information
    training_dataset VARCHAR(500),
    -- Name or description of the training dataset
    -- Examples: "Unspecified unreleased", "Eurus-2-RL-Data", "Unspecified unreleased"
    
    training_dataset_size_datapoints BIGINT,
    -- Size of training dataset in datapoints/tokens
    -- Examples: 13200000000000 (13.2T tokens), 30000000000000 (30T tokens)
    
    dataset_size_notes TEXT,
    -- Additional notes about dataset size
    -- Examples: "13.2 trillion tokens", "more than 30 trillion tokens"
    
    -- Confidence and sources
    confidence VARCHAR(50),
    -- Confidence level in the reported information
    -- Examples: "Confident", "Likely", "Unknown", "Speculative"
    
    link TEXT,
    -- Primary URL link to the model information
    -- Examples: "https://deepmind.google/models/veo/", "https://openai.com/index/introducing-gpt-4-5/"
    
    reference TEXT,
    -- Reference title or paper name
    -- Examples: "Our state-of-the-art video generation model", "Introducing GPT-4.5"
    
    citations INTEGER,
    -- Number of citations (if available)
    -- Examples: 0, 30, 9
    
    authors TEXT,
    -- List of authors who developed the model
    -- Can be very long, containing multiple names separated by commas
    
    abstract TEXT,
    -- Abstract or description of the model's capabilities and innovations
    -- Detailed text describing the model's features and improvements
    
    -- Organization details
    organization_categorization VARCHAR(100),
    -- Type of organization
    -- Examples: "Industry", "Academia", "Industry,Academia"
    
    country_of_organization TEXT,
    -- Country or countries where the organization is based
    -- Examples: "United States of America", "China", "United States of America,China"
    
    -- Performance and notability
    notability_criteria VARCHAR(100),
    -- Criteria for why this model is notable
    -- Examples: "SOTA improvement", "Training cost", "Significant use"
    
    notability_criteria_notes TEXT,
    -- Detailed explanation of notability
    -- Examples: "Described by OpenAI as a 'new order of magnitude of compute'"
    
    -- Training details
    epochs DECIMAL(10,2),
    -- Number of training epochs
    -- Examples: 3.0, 1.0
    
    training_time_hours DECIMAL(15,2),
    -- Total training time in hours
    -- Examples: 2160.0, 130.5, 2400.0
    
    training_time_notes TEXT,
    -- Additional notes about training time
    -- Examples: "512 H100 GPUs were used for three months", "Estimated to be between 3 and 4 months"
    
    -- Hardware information
    training_hardware VARCHAR(200),
    -- Type of hardware used for training
    -- Examples: "NVIDIA H100 SXM5 80GB", "Huawei Ascend 910B"
    
    hardware_quantity DECIMAL(10,2),
    -- Number of hardware units used
    -- Examples: 8192.0, 512.0, 100000.0
    
    hardware_utilization DECIMAL(5,4),
    -- Hardware utilization rate
    -- Examples: 0.3156, 0.4
    
    -- Cost information
    training_compute_cost_usd DECIMAL(15,2),
    -- Training compute cost in 2023 USD
    -- Examples: 6426121.28, 703248.43, 137435820.25
    
    compute_cost_notes TEXT,
    -- Additional notes about compute costs
    
    training_power_draw_w INTEGER,
    -- Training power draw in Watts
    
    -- Model relationships
    base_model VARCHAR(255),
    -- Base model that this model is built upon
    -- Examples: "EXAONE 3.5 32B", "Qwen2.5-Math-7B-Base", "Qwen2.5-7B"
    
    finetune_compute_flop DECIMAL(30,10),
    -- Compute used for fine-tuning in FLOP
    -- Examples: 7.04e+21
    
    finetune_compute_notes TEXT,
    -- Notes about fine-tuning compute
    
    -- Training configuration
    batch_size INTEGER,
    -- Training batch size
    -- Examples: 32000
    
    batch_size_notes TEXT,
    -- Additional notes about batch size
    
    -- Accessibility information
    model_accessibility VARCHAR(100),
    -- How the model can be accessed
    -- Examples: "API access", "Open weights (unrestricted)", "Hosted access (no API)"
    
    training_code_accessibility VARCHAR(100),
    -- Availability of training code
    -- Examples: "Unreleased", "Open source"
    
    inference_code_accessibility VARCHAR(100),
    -- Availability of inference code
    -- Examples: "Unreleased", "Open source"
    
    accessibility_notes TEXT,
    -- Additional notes about accessibility
    -- Examples: "https://huggingface.co/Qwen/QwQ-32B Apache 2", "Creative Commons Attribution Non Commercial 4.0"
    
    -- Technical specifications
    numerical_format VARCHAR(50),
    -- Numerical format used by the model
    -- Examples: "BF16", "FP16"
    
    frontier_model BOOLEAN
    -- Whether this is considered a frontier model
    -- Examples: TRUE, FALSE
);

-- Create indexes for commonly queried fields
CREATE INDEX idx_ai_models_publication_date ON ai_models(publication_date);
CREATE INDEX idx_ai_models_organization ON ai_models(organization);
CREATE INDEX idx_ai_models_domain ON ai_models(domain);
CREATE INDEX idx_ai_models_parameters ON ai_models(parameters);
CREATE INDEX idx_ai_models_notability_criteria ON ai_models(notability_criteria);
CREATE INDEX idx_ai_models_frontier_model ON ai_models(frontier_model);

-- Add comments to the table
COMMENT ON TABLE ai_models IS 'Comprehensive database of notable AI models with their technical specifications, training details, and performance characteristics';
COMMENT ON COLUMN ai_models.model IS 'Official name of the AI model';
COMMENT ON COLUMN ai_models.parameters IS 'Total number of parameters in the model (billions)';
COMMENT ON COLUMN ai_models.training_compute_flop IS 'Total floating point operations used during training';
COMMENT ON COLUMN ai_models.frontier_model IS 'Indicates if this is a state-of-the-art frontier model'; 
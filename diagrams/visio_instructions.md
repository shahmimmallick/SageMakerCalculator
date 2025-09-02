# Creating Visio Diagrams for SageMaker Calculator

## Visio Diagram Creation Guide

### 1. Architecture Diagram (Visio)

**Shapes to Use:**
- **Rectangles**: AWS Services (SageMaker, S3, EC2)
- **Cylinders**: Databases/Storage (S3 buckets)
- **Clouds**: AWS Cloud boundary
- **Arrows**: Data flow connections
- **Diamonds**: Decision points

**Layout Structure:**
```
Top Layer:    [Developer] → [SageMaker Studio] → [JupyterLab]
Middle Layer: [S3 Storage] → [Model Registry] → [SageMaker Endpoint]
Bottom Layer: [Client Apps] → [REST API] → [Python SDK]
```

**Color Scheme:**
- **Orange**: AWS Services
- **Blue**: Data Storage
- **Green**: Application Code
- **Gray**: Infrastructure

### 2. Process Flow Diagram (Visio)

**Flowchart Elements:**
- **Start/End**: Oval shapes
- **Process**: Rectangle shapes
- **Decision**: Diamond shapes
- **Data**: Parallelogram shapes
- **Connector**: Arrow lines

**Flow Steps:**
1. **Start** → Development Phase
2. **Process** → Code Development
3. **Process** → Model Packaging
4. **Process** → S3 Upload
5. **Process** → Endpoint Deployment
6. **Decision** → Deployment Success?
7. **Process** → Testing
8. **End** → Production Ready

### 3. Detailed Component Diagram

**Components to Include:**

#### SageMaker Studio Section:
- JupyterLab Environment
- Notebook Files (.ipynb)
- Python Files (.py)
- Requirements.txt

#### Model Packaging Section:
- Source Files
- Tar.gz Creation
- S3 Upload Process

#### Deployment Section:
- PyTorchModel Creation
- Endpoint Configuration
- Instance Provisioning

#### Runtime Section:
- HTTP Request Flow
- Inference Pipeline
- Response Generation

### 4. Network Architecture Diagram

**Network Components:**
- **VPC**: Virtual Private Cloud boundary
- **Subnets**: Public/Private subnet separation
- **Security Groups**: Firewall rules
- **Load Balancer**: Traffic distribution
- **NAT Gateway**: Outbound internet access

### 5. Data Flow Diagram

**Data Elements:**
- **Input**: JSON Request
- **Processing**: Mathematical Operations
- **Output**: JSON Response
- **Storage**: Model Artifacts
- **Logs**: CloudWatch Logs

## Visio Template Structure

### Page 1: High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    AWS Cloud Environment                    │
│  ┌─────────────┐  ┌─────────────┐  ┌───────────────── ────┐ │
│  │ SageMaker   │  │     S3      │  │    SageMaker         │ │
│  │   Studio    │→ │   Storage   │→ │    Endpoint          │ │
│  └─────────────┘  └─────────────┘  └──────────────────── ─┘ │
│                                              ↓              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Client Applications                       │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Page 2: Detailed Process Flow
```
Start → Code Development → Local Testing → Model Packaging → 
S3 Upload → Endpoint Creation → Deployment → Testing → Production
```

### Page 3: Request/Response Flow
```
Client Request → SageMaker Runtime → Endpoint → Model Server → 
Inference Code → Calculator Logic → Response → Client
```

## Visio Stencils to Download

**AWS Architecture Stencils:**
- AWS Simple Icons
- AWS 3D Icons
- AWS Architecture Icons

**Process Flow Stencils:**
- Basic Flowchart Shapes
- Cross-Functional Flowchart
- Workflow Diagram

**Network Stencils:**
- Network and Peripherals
- Computers and Monitors
- Server Rack

## Step-by-Step Visio Creation

### Step 1: Setup
1. Open Microsoft Visio
2. Choose "AWS Architecture" template
3. Import AWS stencils
4. Set page orientation to Landscape

### Step 2: Create Architecture Diagram
1. Drag AWS Cloud shape to canvas
2. Add SageMaker Studio rectangle
3. Add S3 cylinder for storage
4. Add SageMaker Endpoint rectangle
5. Connect with arrows
6. Add labels and descriptions

### Step 3: Create Flow Diagram
1. Start with oval "Start" shape
2. Add process rectangles for each phase
3. Add decision diamonds where needed
4. Connect with directional arrows
5. Add swimlanes for different actors

### Step 4: Format and Style
1. Apply consistent colors
2. Use AWS orange for services
3. Add shadows and effects
4. Align shapes properly
5. Add title and legend

### Step 5: Add Details
1. Include service names
2. Add instance types (ml.t2.medium)
3. Show file names (inference.py)
4. Include API endpoints
5. Add cost information

## Export Options

**For Documentation:**
- PDF (High Quality)
- PNG (300 DPI)
- SVG (Scalable)

**For Presentations:**
- PowerPoint slides
- JPEG images
- Visio Web format

## Tips for Professional Diagrams

1. **Consistency**: Use same shapes for same types of components
2. **Clarity**: Avoid crossing lines where possible
3. **Hierarchy**: Show relationships clearly
4. **Labels**: Include meaningful names and descriptions
5. **Legend**: Explain colors and symbols used
6. **Spacing**: Maintain consistent spacing between elements
7. **Alignment**: Align shapes to grid for clean appearance